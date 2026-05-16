from fastapi import FastAPI
from app.tt import tt_test
from app.logger import Logger

"""
imports
logger
env setting
lifespan events
app initialization
middleware
global exception handlers
routers
static files
health check
"""

logger = Logger(__name__)
logger.info("test")
tt_test()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
