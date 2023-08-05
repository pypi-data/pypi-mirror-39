import logging
from flask_restplus import Api
from lantern_flask import settings


log = logging.getLogger(__name__)

api = Api(
    version=settings.get("API_VERSION", "1.0"),
    title=settings.get("API_TITLE", "Lantern Engine API"),
    description=settings.get("API_DESC", "Lantern Tech"),
)


@api.errorhandler
def default_error_handler(e):
    """Default Error Handles
    
    Args:
        e (Exception): Any exeption generated
    
    Returns:
        json: A proper json message
    """
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.get("DEBUG", False):
        return {'message': message}, 500
