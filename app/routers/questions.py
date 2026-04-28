from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.question import Question
from app.models.user import User
from app.schemas.test_schema import QuestionResponse, AnswerVerify, AnswerResponse
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(
    topic_id: int = Query(None),
    difficulty: str = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    return query.limit(limit).all()

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/verify", response_model=AnswerResponse)
def verify_answer(
    data: AnswerVerify,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == data.question_id).first()
    if not question:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")

    from app.models.question import QuizAttempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        question_id=data.question_id,
        selected_option=data.selected_option,
        is_correct=(data.selected_option == question.correct_option)
    )
    db.add(attempt)
    db.commit()

    return AnswerResponse(
        is_correct=(data.selected_option == question.correct_option),
        correct_option=question.correct_option,
        explanation=question.explanation
    )
