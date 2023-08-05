from lantern_flask import settings

class ApplicationController(object):
    """ Allow us to easily fetch cognito parsed data 
    """

    def __init__(self, debug=False):
        self.debug = debug if debug else settings.get("LOCAL_USER", False)

    def get_app_id(self, request, required=True):
        """ Returns the app_id value sent in the request headers
            Parameters:
                - request: required, active HTTP request
                - required: (default=True) if set to True and no app_id foud a ValueError will be raised
        """
        if not request:
            raise Exception(
                "You have to specify a valid `request` parameter (inside a http request)")
        
        app_id_value = request.headers.get("app_id", None)

        return app_id_value
