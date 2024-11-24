import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseHandler:

    def __init__(self, base, handler, storage, identifier=None, request_body=None):
        logger.info(f'Entered base handler, processing base: {base}, handler: {handler}')
        self.request_body = request_body
        self.identifier = identifier
        self.storage = storage
        self.results = {}

        logger.info(f'Calling base: {base}, handler: {handler} process function')
        self.process()

    def process():
        # overriden by child class to support factory design pattern
        logger.error('Generic process function called, factory pattern implemented incorrectly')
