from pydantic import BaseModel
from typing import List, Optional

class HeadlineTextPair(BaseModel):
    headline: str
    text: str

class Post(BaseModel):
    title: str
    author: str
    content: List[HeadlineTextPair]

class Podcast(BaseModel):
    title: str
    url: str
    author: str
    description: str
    timecode: str
