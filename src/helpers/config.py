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

    # ====== LLM =======
    GENERATION_BACKEND :str
    GENERATION_BACKEND2 :str
    EMBEDDING_BACKEND :str

    OPENAI_API_KEY :str = None
    OPENAI_API_URL :str = None
    GENERATION_MODEL_ID_OPENAI :str = None

    GEMINI_API_KEY :str = None
    GENERATION_MODEL_ID_GEMINI :str = None

    COHERE_API_KEY :str = None
    EMBEDDING_MODEL_ID_COHERE :str = None
    EMBEDDING_MODEL_SIZE_COHERE : int  = None

    EMBEDDING_MODEL_ID_GEMINI :str  = None
    EMBEDDING_MODEL_SIZE_GEMINI : int = None

    INPUT_DAFAULT_MAX_CHARACTERS : int = None
    GENERATION_DEFAULT_MAX_TOKENS : int = None
    GENERATION_DEFAULT_TEMPERATURE : float  = None


    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_DISTANCE_METHOD: str = None

    
    class Config :
        env_file ='.env'


def app_setting():
    return Setting()