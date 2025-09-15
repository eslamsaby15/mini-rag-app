from pydantic import BaseModel
from typing import Optional

class DataRequest(BaseModel) : 
    file_id :  Optional[str]
    chunk_size : Optional[int] = 150
    chunk_overlap : Optional[int] = 50
    do_reset : Optional[int] = 0