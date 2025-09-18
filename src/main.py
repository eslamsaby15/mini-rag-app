from fastapi import FastAPI 
from routers import base_router ,data_router ,nlp_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import app_setting

from stores.llm.Providerfactory import LLMProviderFactory
from stores.vectorDB.VectorDbFactory import VectorDBProviderFactory
app = FastAPI()

@app.on_event('startup') 
async def start_DB(): 
      setting = app_setting()
      app.mongon_connection = AsyncIOMotorClient(setting.MONGODB_URL)
      app.db_client= app.mongon_connection[setting.MONGODB_DATABASE]

      llm_provider_factory = LLMProviderFactory(setting)
      vectordb_provider_factory = VectorDBProviderFactory(setting)

      # generation client
      app.generation_client = llm_provider_factory.create(provider=setting.GENERATION_BACKEND2)
      app.generation_client.set_generation_model(model_id = setting.GENERATION_MODEL_ID_GEMINI)

      # embedding client
      app.embedding_client = llm_provider_factory.create(provider=setting.EMBEDDING_BACKEND)
      app.embedding_client.set_embedded_model(model_id=setting.EMBEDDING_MODEL_ID_COHERE,
                                                embedding_size=setting.EMBEDDING_MODEL_SIZE_COHERE)

      app.vectordb_client = vectordb_provider_factory.create(
         provider=setting.VECTOR_DB_BACKEND
      )
      app.vectordb_client.connect()
      



@app.on_event('shutdown') 
async def shuddown(): 
   app.mongon_connection.close()
   app.vectordb_client.disconnect()

app.include_router(base_router)
app.include_router(data_router)
app.include_router(nlp_router)