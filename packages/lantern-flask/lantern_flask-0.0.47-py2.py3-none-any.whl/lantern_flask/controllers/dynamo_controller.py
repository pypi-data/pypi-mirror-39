import boto3
import logging
import time
from lantern_flask import settings
from lantern_flask.utils.json import json_float_to_decimal
from lantern_flask.utils.request import http_response, http_error
from lantern_flask.controllers.application_controller import ApplicationController
from lantern_flask.controllers.cognito_controller import CognitoController
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
log = logging.getLogger(__name__)


class ExceptionInvalidDynamoControllerType(Exception):
    """ Dynamo Type Not defined, this is a programming error """
    pass


class ExceptionInvalidDynamoControllerNotFound(Exception):
    """ Object not found in DB (404 error) """
    pass


class DynamoController(object):
    """ Generic Dynamo Access Controller
        - Error handling
        - response message/data normalization
    """

    TYPE_GET = "get"
    TYPE_CREATE = "create"
    TYPE_UPDATE = "update"
    TYPE_DELETE = "delete"
    TYPE_FILTER = "filter"

    ORDER_ASC = "asc"
    ORDER_DESC = "desc"

    controller_app = None
    controller_cognito = None


    def __init__(self, table_name, filter_app=False, debug=False):
        """ Initialize Dynamo Controller

        Arguments:
            table_name {str} -- Dynamo table name
            filter_by_username {bool} -- If true, this controller will filter and validate username in session with handled records.
        """
        self.debug = debug if debug else settings.get("LOCAL_USER", False)
        self.filter_app = filter_app
        self.table = dynamodb.Table(table_name)
        self.controller_app = ApplicationController(debug=self.debug)
        self.controller_cognito = CognitoController()

    def get(self, primary_keys, request=None, return_raw=False):
        """ return a the first element corresponding to the filter_data param
            Parameters:
                - filter_app: boolean, if set to True, app_id will be verified in the response
        """
        res = self._execute_operation(type=self.TYPE_GET, primary_keys=primary_keys, request=request, return_raw=return_raw)
        if return_raw:
            return res
        else:
            return res, res["status"]

    def create(self, data, return_raw=False):
        """ Creates a new instance in the DB.
            - Overrides by primary key)
            - Returns the new/updated element
        """
        res = self._execute_operation(type=self.TYPE_CREATE, data=data, return_raw=return_raw)
        if return_raw:
            return res
        else:
            return res, res["status"]

    def update(self, primary_keys, data, request=None, return_raw=False):
        """ Update an existing object in the database
            - Returns the updated object
        """
        res = self._execute_operation(type=self.TYPE_GET, request=request, primary_keys=primary_keys)
        if res["status"] != 200:
            return res
        res = self._execute_operation(type=self.TYPE_UPDATE, primary_keys=primary_keys, data=data, request=request, return_raw=return_raw)
        if return_raw:
            return res
        else:
            return res, res["status"]

    def delete(self, primary_keys, request=None, return_raw=False):
        """ Deletes a set of objects, corresponding to filter_data
            - Delete the specific element
        """
        res = self._execute_operation(type=self.TYPE_GET, primary_keys=primary_keys, request=request)
        if res["status"] != 200:
            return res
        res = self._execute_operation(type=self.TYPE_DELETE, primary_keys=primary_keys, request=request, return_raw=return_raw)
        if return_raw:
            return res
        else:
            return res, res["status"]


    def filter(self, key, value, order_by=None, limit=None, next=None, index=None, order_type=ORDER_DESC, filter_expression=None, request=None, return_raw=False):
        """ Return all orders related to this user
            Params:
                - filter_expression is of type: FilterExpression (boto3), Veryyy flexible
                - first_element: Boolean, if set to True it will return the first element in the query of 404
                - filter_app: Boolean, if set to True, request is requiered and filter_expression will be overrided to filter by app_id
                    - Exception: if no request is provided
                    - ValueError: is filter_expression has a value
        """
        if index:
            index_name = index
        elif key and order_by:
            index_name = "{}-{}-index".format(key, order_by)
        else:
            index_name = "{}-index".format(key)

        params = {
            "IndexName": index_name,
            "KeyConditionExpression": Key(key).eq(value)
        }
        if next:
            params["ExclusiveStartKey"] = next
        
        if filter_expression:
            params["FilterExpression"] = filter_expression

        request_limit = self._get_request_limit(request,limit)
        params["Limit"] = request_limit
        # Filtering by app
        if self.filter_app == True:
            app_id = self.controller_app.get_app_id(request=request)
            if not app_id:
                raise Exception("No app_id provided in the HTTP header")
            if not request:
                raise Exception("A Active request is required if you want to filter by app")
            if filter_expression:
                raise ValueError("You provided a filter_expression and filter_app, filter_app requires to override filter expression (you can't use both)")
            filter_expression = Key("app_id").eq(app_id)

        if request and order_by:
            time_filter,order = self._get_request_parameters(request)
            order_type = order if order else order_type

            if(order_by == "timestamp"):
                params["KeyConditionExpression"] = time_filter & Key(key).eq(value) if time_filter else Key(key).eq(value)
            else:
                if filter_expression:
                    params["FilterExpression"] = filter_expression & time_filter if time_filter else filter_expression
                else:
                    params["FilterExpression"] = time_filter if time_filter else None

        if order_type == self.ORDER_DESC:
            params["ScanIndexForward"] = False

        res = self._execute_operation(type=self.TYPE_FILTER, primary_keys=params, return_raw=return_raw)
        if return_raw:
            return res
        else:
            return res, res["status"]

    def _get_request_parameters(self,request):
        """ Get order, initial timestamp and final timestamp from request
        """
        order               = request.args.get("order", None)
        initial_timestamp   = request.args.get("initial_timestamp", None)
        final_timestamp     = request.args.get("final_timestamp", None)

        if not final_timestamp and initial_timestamp:
            filter_expression   = Key('timestamp').gt(int(initial_timestamp))

        if not initial_timestamp and final_timestamp:
            filter_expression   = Key('timestamp').lt(int(final_timestamp))

        if not initial_timestamp and not final_timestamp:
            filter_expression   = None

        if initial_timestamp and final_timestamp:
            filter_expression   = Key('timestamp').between(int(initial_timestamp), int(final_timestamp))

        return filter_expression,order

    def _get_request_limit(self,request,limit):
        if limit:
            return limit
        else:
            request_limit = request.args.get("limit", None)
            if request_limit:
                return int(request_limit)
            else:
                return 100


    def _execute_operation(self, type, primary_keys=None, data=None, request=None, return_raw=False):
        """ Execute the dynamo operation and return a proper response (success or error)
        """
        try:
            if type == self.TYPE_GET:
                d_res = self.table.get_item(Key=primary_keys)
                if "Item" in d_res:
                    data = d_res["Item"]
                else:
                    raise ExceptionInvalidDynamoControllerNotFound("Not Found")
                # Filter by app
                if self.filter_app == True:
                    app_id = self.controller_app.get_app_id(request=request)
                    if not app_id:
                        raise Exception("No app_id provided in the HTTP header")
                    if "app_id" in data and data["app_id"] != app_id:
                        raise ExceptionInvalidDynamoControllerNotFound("element found in another app_id")
                code = d_res['ResponseMetadata']['HTTPStatusCode']
                return data if return_raw else http_response(code=code, message="Fetched", data=data)
            elif type == self.TYPE_CREATE:
                data = json_float_to_decimal(data)
                d_res = self.table.put_item(Item=data)
                code = d_res['ResponseMetadata']['HTTPStatusCode']
                return data if return_raw else http_response(code=code, message="Created", data=data)
            elif type == self.TYPE_UPDATE:
                data = json_float_to_decimal(data)
                d_res = self.table.update_item(
                    Key=primary_keys,
                    UpdateExpression="set " + ", ".join(["{} = :_{}".format(key,key) for key in data.keys()]),
                    ExpressionAttributeValues={ ":_{}".format(key): data[key] for key in data.keys() },
                    ReturnValues="UPDATED_NEW")
                code = d_res['ResponseMetadata']['HTTPStatusCode']
                return data if return_raw else http_response(code=code, message="Updated", data=data)
            elif type == self.TYPE_DELETE:
                d_res = self.table.delete_item(Key=primary_keys)
                code = d_res['ResponseMetadata']['HTTPStatusCode']
                return data if return_raw else http_response(code=code, message="Deleted", data=primary_keys)
            elif type == self.TYPE_FILTER:
                response = self.table.query(**primary_keys)
                data = response["Items"] if response["Count"] != 0 else []
                code = response['ResponseMetadata']['HTTPStatusCode']
                count = response["Count"]
                next = response["LastEvaluatedKey"] if "LastEvaluatedKey" in response else None
                return data if return_raw else http_response(code=code, message="Filtered", data=data, count=count, next=next)
            else:
                raise ExceptionInvalidDynamoControllerType(
                    "Type {} not defined in DynamoController".format(type))
        except ExceptionInvalidDynamoControllerType as e:
            return http_error(code=500, message="Type not defined in controller", detail=str(e))
        except ExceptionInvalidDynamoControllerNotFound as e:
            return http_error(code=404, message="Element Not Found", detail=str(e))
        except Exception as e:
            if self.debug:
                raise e
            return http_error(code=500, message="Unexpected error", detail=str(e))
