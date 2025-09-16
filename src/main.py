from fastapi import FastAPI 
from routers import base_router ,data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import app_setting

app = FastAPI()

@app.on_event('startup') 
async def start_DB(): 
    setting = app_setting()
    app.mongon_connection = AsyncIOMotorClient(setting.MONGODB_URL)
    app.db_client= app.mongon_connection[setting.MONGODB_DATABASE]

@app.on_event('shutdown') 
async def shuddown(): 
   app.mongon_connection.close()

app.include_router(base_router)
app.include_router(data_router)