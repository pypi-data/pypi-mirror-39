from lantern_flask.utils.json import json_decimal_to_float, json_float_to_decimal

SYSTEM_COLUMNS = ["username", "app_id"]

def fn_cleanup_system_cols(data):
    """ Remove System columns from all returned objects
    """
    is_list = True if isinstance(data, list) else False
    data_total = data if is_list else [data]
    for record in data_total:
        for col in SYSTEM_COLUMNS:
            if col in record:
                del record[col]
    return data_total if is_list else data_total[0]


def http_response(code, message, data, count=None, next=None, response=None, cleanup_system_cols=True, convert_json_decimal_to_float=True):
    """ Format a return a valid JSON
    
    Arguments:
        code {int} -- Valid HTTP Status Code
        message {str} -- Message to be sent
        data {json} -- Json to be returned
    
    Keyword Arguments:
        count {int} -- count if we return multiple values (default: {None})
        next {json} -- current search index, for pagination (default: {None})
        response {res} -- a valid http response (default: {None})
    
    Returns:
        [type] -- [description]
    """
    data = json_decimal_to_float(data) if convert_json_decimal_to_float else data
    data_json = {
        "status": code,
        "message": message,
        "results": fn_cleanup_system_cols(data) if cleanup_system_cols else data,
    }
    if count:
        data_json["count"] = count
    if next:
        data_json["next"] = json_decimal_to_float(next)
    if response:
        data_json["raw"] = response
    return data_json


def http_error(code, message, detail, e=None):
    """ return a standard json response for errors """
    data = {
        "status": code,
        "message": message,
        "detail": detail,
    }
    if e:
        data["raw"] = str(e)
    return data