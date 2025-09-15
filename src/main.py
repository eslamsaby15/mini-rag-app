from fastapi import FastAPI 
from routers import base_router


app = FastAPI()

app.include_router(base_router)