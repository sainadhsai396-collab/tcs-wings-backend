from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    starter_code = Column(Text)
    solution_code = Column(Text)
    expected_output = Column(Text)
    hints = Column(JSON)
    difficulty = Column(String, default="medium")
    duration_minutes = Column(Integer)
    order_index = Column(Integer, default=0)

    topic = relationship("Topic", back_populates="labs")
    submissions = relationship("LabSubmission", back_populates="lab")

class LabSubmission(Base):
    __tablename__ = "lab_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(Integer, ForeignKey("labs.id"))
    submitted_code = Column(Text, nullable=False)
    output = Column(Text)
    is_correct = Column(Boolean)
    submitted_at = Column(String)

    user = relationship("User", back_populates="lab_submissions")
    lab = relationship("Lab", back_populates="submissions")
