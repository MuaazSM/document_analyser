from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Dict, Any


class Metadata(BaseModel):
    Summary: List[str]
    Title: str
    Author: List[str]
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    # PageCount: Union[int, str]  # Can be "Not Available"
    SentimentTone: str


class ChangeFormat(BaseModel):
    Page:str
    changes:str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass