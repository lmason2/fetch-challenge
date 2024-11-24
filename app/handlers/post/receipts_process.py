from handlers.base_handler import BaseHandler
import logging
from uuid import uuid4
from handlers.utils import validate_receipt
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReceiptsProcessHandler(BaseHandler):
    
    def process(self):
        logger.info(f'Entered process function for receipts process handler, validating receipt')
        if not validate_receipt(self.request_body):
            raise HTTPException(status_code=400, detail='The receipt is invalid')

        receipt_id = str(uuid4())

        logger.info(f'Updating storage with receipt id: {receipt_id}')
        self.storage.update({
            receipt_id: self.request_body
        })
        
        self.results.update({
            'id': receipt_id
        })
