from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from factory import HandlerFactory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

store = {}

@app.get('/{base}/{identifier}/{handler}')
async def handle(base, identifier, handler):
    logger.info(f'Entered get handler with base: {base}, identifier: {identifier}, and handler: {handler}')
    try:
        handler_class = HandlerFactory.handle_route(base, handler, store, identifier)
        return JSONResponse(content=handler_class.results, status_code=200)
    except HTTPException as http_exception:
        logger.error(f'''HTTP Exception caught in get handler endpoint: 
                     detail - {http_exception.detail}, 
                     status - {http_exception.status_code}''')
        raise HTTPException(status_code=http_exception.status_code, detail=http_exception.detail)
    except Exception as general_exception:
        logger.error(f'General exception caught in get handler: {general_exception}')
        raise HTTPException(status_code=500)


@app.post('/{base}/{handler}')
async def handle(base, handler, request: Request):
    try:
         request_body = await request.json()
         handler_class = HandlerFactory.handle_route(base, handler, store, request=request_body)
         return JSONResponse(content=handler_class.results, status_code=200)
    except HTTPException as http_exception:
        logger.error(f'''HTTP Exception caught in post handler endpoint: 
                     detail - {http_exception.detail}, 
                     status - {http_exception.status_code}''')
        raise HTTPException(status_code=http_exception.status_code, detail=http_exception.detail)
    except Exception as general_exception:
        logger.error(f'General exception caught in post handler: {general_exception}')
        raise HTTPException(status_code=500)
