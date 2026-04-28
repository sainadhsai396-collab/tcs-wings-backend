from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exam import MockExam
from app.models.user import User
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/api/exams", tags=["exams"])

@router.get("")
def get_exams(db: Session = Depends(get_db)):
    return db.query(MockExam).filter(MockExam.is_active == True).all()

@router.get("/{exam_id}")
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(MockExam).filter(MockExam.id == exam_id).first()
    if not exam:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
