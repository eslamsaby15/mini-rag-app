from pydantic import BaseModel , Field , validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel) : 
    id : Optional[ObjectId] = Field(None, alias='_id')
    project_id : str = Field(...,min_length=1)

    @validator('project_id')
    def valid_prokect_id(cls , value):
        if  not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    @classmethod
    def get_indexes(cls):
        return [{'key' :[("project_id", 1)] , 
                'name' :'project_if_index_1' ,
                'unique' :True}]
        
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
