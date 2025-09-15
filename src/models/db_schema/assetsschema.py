from pydantic import BaseModel , Field , validator
from typing import Optional 
from bson.objectid import ObjectId
from datetime import datetime

class AssetsSchema(BaseModel) : 
    id : Optional[ObjectId] = Field(None, alias='_id')
    asset_name :str = Field(...,min_length=1)
    asset_size : int = Field(None, gt =0)
    asset_config :dict =Field(default= None)
    asset_pushed_at : datetime = Field(default=datetime.utcnow)


    @classmethod 
    def get_indexes(cls):
        return [{'key' : [('asset_project_id' ,1 )] , 
                 'name' :"asset_project_id_index_1" , 
                 'unique' :False},

                 {'key' : [('asset_project_id' ,1) ,
                           ('asset_name',1)] , 
                 'name' :"asset_project_id_name_index_1" , 
                 'unique' :True}]
        
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True