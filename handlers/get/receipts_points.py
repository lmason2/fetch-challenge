from handlers.base_handler import BaseHandler
import logging
from fastapi import HTTPException
from handlers.utils import determine_points

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReceiptsPointsHandler(BaseHandler):

    def process(self):
        logger.info('Entered process function for receipts points handler')
        logger.info(f'Looking for receipt id: {self.identifier} in storage')

        receipt = self.storage.get(self.identifier, None)
        if receipt is None:
            logger.error(f'Receipt with provided id: {self.identifier} not found')
            raise HTTPException(status_code=404, detail='No receipt found for that id')
    
        self.results = {'points': determine_points(receipt)}
