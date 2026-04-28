from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class StudyPlanDay(Base):
    __tablename__ = "study_plan_days"

    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    day_topic = Column(String, nullable=False)
    topics = Column(JSON)
    objectives = Column(JSON)
    lab_exercises = Column(JSON)
    estimated_hours = Column(Float, default=4.0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(String)

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    status = Column(String, default="not_started")
    progress_percent = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    notes = Column(Text)
    completed_at = Column(String)

    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
