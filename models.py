from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BlogPost(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=3, max_length=50)
    published: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UpdateBlogPost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author: Optional[str]
    published: Optional[bool]
