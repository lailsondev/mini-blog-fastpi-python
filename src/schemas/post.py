from pydantic import BaseModel, AwareDatetime, NaiveDatetime
from typing import Optional


class PostIn(BaseModel):
    title: str
    content: str
    published_at: AwareDatetime | NaiveDatetime | None = None
    published: bool = False
 
 
class PostUpdateIn(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    published_at: Optional[AwareDatetime | NaiveDatetime] = None