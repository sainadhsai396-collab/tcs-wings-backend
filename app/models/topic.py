from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String)
    category = Column(String)
    order_index = Column(Integer, default=0)

    lessons = relationship("Lesson", back_populates="topic")
    questions = relationship("Question", back_populates="topic")
    labs = relationship("Lab", back_populates="topic")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content = Column(Text)
    content_type = Column(String, default="markdown")
    duration_minutes = Column(Integer)
    order_index = Column(Integer, default=0)

    topic = relationship("Topic", back_populates="lessons")
    progress = relationship("UserProgress", back_populates="lesson")
