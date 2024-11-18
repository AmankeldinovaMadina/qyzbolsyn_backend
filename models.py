from pydantic import BaseModel
from typing import List, Optional

class HeadlineTextPair(BaseModel):
    headline: str
    text: str

class TimecodePair(BaseModel):
    time: str
    label: str

class Post(BaseModel):
    title: str
    author: str
    category: str
    content: List[HeadlineTextPair]

class Podcast(BaseModel):
    title: str
    url: str
    author: str
    category: str
    description: str
    timecode: List[TimecodePair]
    video_length: str



class User(BaseModel):
    email: str
    password: str = None  # Optional in case of Google or Apple login


class MessageRequest(BaseModel):
    message: str