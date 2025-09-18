from helpers.config import Setting , app_setting
from .providers import QdrantDB
from .vectordbEnum import VectorDBEnums
from controllers.BaseController import BaseModelController

class VectorDBProviderFactory :
    def __init__(self , config  :Setting):
        self.config = config
        self.base_controller = BaseModelController()
        pass

    def create(self,provider : str ): 
        if provider == VectorDBEnums.QDRANT.value : 
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDB(db_path=db_path ,
                        distance_method= self.config.VECTOR_DB_DISTANCE_METHOD )

        return None
