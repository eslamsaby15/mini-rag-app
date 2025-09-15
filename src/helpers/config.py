from pydantic_settings import BaseSettings

from typing import Optional

class Setting(BaseSettings) : 
    APP_NAME :str
    APP_VERSION:str
    APP_CREATOR:str
    GOOGLE_API_KEY: Optional[str] = None
    LANGSMITH_API_KEY:Optional[str] = None

    class Config :
        env_file ='.env'


def app_setting():
    return Setting()