import logging
import os
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from ..config import app_config

log = logging.getLogger(__name__)

api = Api(version='1.0', title='BIONS Device lodgings',
          description='Make the most out of your crucial investments by integrating remote monitoring and maintenance into your enterprise processes. Enable new ways to create compelling and innovative services. Monitor your mission-critical assets, prevent costly breakdowns, improve customer service, and create new business opportunities and service-level agreement')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not app_config[os.getenv('FLASK_ENV')].DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
