from fastapi import FastAPI 
from routers import base_router ,data_router


app = FastAPI()

app.include_router(base_router)
app.include_router(data_router)