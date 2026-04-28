from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.study_plan import UserProgress
from app.models.question import QuizAttempt
from app.services.auth_service import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("")
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    completed_lessons = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.status == "completed"
    ).count()

    total_quizzes = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).count()

    correct_quizzes = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.is_correct == True
    ).count()

    return {
        "completed_lessons": completed_lessons,
        "total_quizzes": total_quizzes,
        "correct_quizzes": correct_quizzes,
        "accuracy": round(correct_quizzes / total_quizzes * 100, 1) if total_quizzes > 0 else 0
    }

@router.post("/lesson/{lesson_id}")
def update_lesson_progress(
    lesson_id: int,
    status: str = "in_progress",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == lesson_id
    ).first()

    if progress:
        progress.status = status
        if status == "completed":
            progress.completed_at = datetime.utcnow().isoformat()
    else:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status=status,
            completed_at=datetime.utcnow().isoformat() if status == "completed" else None
        )
        db.add(progress)

    db.commit()
    return {"status": "updated"}
