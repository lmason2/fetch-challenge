import logging
from handlers.get.receipts_points import ReceiptsPointsHandler
from handlers.post.receipts_process import ReceiptsProcessHandler
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler_map = {
    'receipts': {
        'points': ReceiptsPointsHandler,
        'process': ReceiptsProcessHandler
    }
}


class HandlerFactory:

    @staticmethod
    def handle_route(base, handler, storage, identifier=None, request=None):
        try:
            handler_class = handler_map.get(base, {}).get(handler, None)

            if handler_class is None:
                logger.info(f'Base: {base}, handler: {handler} not found, returning 404')
                raise HTTPException(status_code=404)
            
            return handler_map.get(base).get(handler)(base, handler, storage, identifier, request)
        except HTTPException as http_error:
            logger.error(f'''Caught http exception processing handler with base: {base}, handler: {handler}. 
                         Detail - {http_error.detail} 
                         Status Code - {http_error.status_code}''')
            raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
        except Exception as general_exception:
            logger.error(f'''Caught general exception in factory handler, raising as 500. 
                         Error: {general_exception}''')
            raise HTTPException(status_code=500)
            

