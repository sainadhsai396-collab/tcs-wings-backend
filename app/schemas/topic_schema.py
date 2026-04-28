from pydantic import BaseModel
from typing import Optional

class TopicBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None

class TopicResponse(TopicBase):
    id: int
    order_index: int

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None
    content_type: str = "markdown"
    duration_minutes: Optional[int] = None

class LessonResponse(LessonBase):
    id: int
    topic_id: int
    order_index: int

    class Config:
        from_attributes = True
