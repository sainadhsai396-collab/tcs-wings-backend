from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class MockExam(Base):
    __tablename__ = "mock_exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    passing_marks = Column(Integer)
    is_active = Column(Boolean, default=True)

    attempts = relationship("ExamAttempt", back_populates="exam")
    sections = relationship("ExamSection", back_populates="exam")

class ExamSection(Base):
    __tablename__ = "exam_sections"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("mock_exams.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    questions_count = Column(Integer, nullable=False)
    marks_per_question = Column(Integer, default=1)

    exam = relationship("MockExam", back_populates="sections")

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_id = Column(Integer, ForeignKey("mock_exams.id"))
    started_at = Column(String)
    completed_at = Column(String)
    score = Column(Integer)
    total_marks = Column(Integer)
    time_taken_seconds = Column(Integer)
    answers = Column(JSON)

    user = relationship("User", back_populates="exam_attempts")
    exam = relationship("MockExam", back_populates="attempts")
