from pydantic_settings import BaseSettings

from typing import Optional

class Setting(BaseSettings) : 
    APP_NAME :str
    APP_VERSION:str
    APP_CREATOR:str
    GOOGLE_API_KEY: Optional[str] = None
    LANGSMITH_API_KEY:Optional[str] = None
    FILE_ALLOW_TYPES:list[str]
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int
    MONGODB_URL:str
    MONGODB_DATABASE:str
    class Config :
        env_file ='.env'


def app_setting():
    return Setting()