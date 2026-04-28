from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    explanation = Column(Text)
    difficulty = Column(String, default="medium")
    marks = Column(Integer, default=1)

    topic = relationship("Topic", back_populates="questions")
    attempts = relationship("QuizAttempt", back_populates="question")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option = Column(String)
    is_correct = Column(Boolean)
    answered_at = Column(String)

    user = relationship("User", back_populates="quiz_attempts")
    question = relationship("Question", back_populates="attempts")
