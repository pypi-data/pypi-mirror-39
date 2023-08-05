import logging
from flask import Blueprint
from flask_cors import CORS

from lantern_flask import api
log = logging.getLogger(__name__)

class Router(object):
    """ Routing for flask and blueprint
    """

    api = None
    endpoints = []

    def __init__(self, path, description="", use_cors=True):
        self.api = api
        self.path = path
        self.description = description
        self.use_cors = use_cors

    def init(self, flask_app):
        """ Initialize the app, called from entry point """
        blueprint = Blueprint('api', __name__)
        self.api.init_app(blueprint)
        self._init_endpoints()
        if self.use_cors:
            CORS(flask_app)
        flask_app.register_blueprint(blueprint)

    def register(self, fn):
        """ Add a new function for registering that endpoint
        """
        self.endpoints.append(fn)

    def _get_namespace(self):
        return self.api.namespace(self.path, description=self.description)
    
    def _init_endpoints(self):
        ns = self._get_namespace()
        for fn in self.endpoints:
            fn(ns=ns, api=self.api)
