from fastapi import FastAPI
from fastapi.requests import Request
from typing import Callable
import time
import logging


# logger = logging.getLogger("uvicorn.access")
# logger.disabled = True

def register_middelware(app: FastAPI):
    
    @app.middleware("http")
    async def custom_logging(request: Request, func_call: Callable):
        start = time.time()
        print(f"Calling Function - {func_call.__name__} for request - {request.url}")
        response = await func_call(request)
        print(f"Function Executed in {time.time() - start} seconds.")
        return response