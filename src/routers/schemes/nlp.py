from pydantic import BaseModel
from typing import Optional

class PushReqScema(BaseModel): 
    do_reset : Optional[int] = 0


class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 5