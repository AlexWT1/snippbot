from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SnippetBase(BaseModel):
    name: str
    content: str

class SnippetCreate(SnippetBase):
    pass

class Snippet(SnippetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True