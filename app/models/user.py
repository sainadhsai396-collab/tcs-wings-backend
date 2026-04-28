from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    progress = relationship("UserProgress", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    lab_submissions = relationship("LabSubmission", back_populates="user")
    exam_attempts = relationship("ExamAttempt", back_populates="user")
    streak = relationship("StudyStreak", back_populates="user", uselist=False)

class StudyStreak(Base):
    __tablename__ = "study_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    streak_count = Column(Integer, default=0)
    last_study_date = Column(String)
    longest_streak = Column(Integer, default=0)

    user = relationship("User", back_populates="streak")
