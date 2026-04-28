from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.topic import Topic, Lesson
from app.schemas.topic_schema import TopicResponse, LessonResponse
from typing import List

router = APIRouter(prefix="/api/topics", tags=["topics"])

@router.get("", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).order_by(Topic.order_index).all()
    return topics

@router.get("/{slug}", response_model=TopicResponse)
def get_topic(slug: str, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.get("/{slug}/lessons", response_model=List[LessonResponse])
def get_topic_lessons(slug: str, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Topic not found")
    lessons = db.query(Lesson).filter(Lesson.topic_id == topic.id).order_by(Lesson.order_index).all()
    return lessons

@router.get("/lesson/{slug}", response_model=LessonResponse)
def get_lesson(slug: str, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
