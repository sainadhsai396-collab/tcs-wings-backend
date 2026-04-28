from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.study_plan import StudyPlanDay
from app.services.study_plan_service import generate_38_day_plan
from typing import List, Optional

router = APIRouter(prefix="/api/study-plan", tags=["study_plan"])

def ensure_plan_exists(db: Session):
    existing = db.query(StudyPlanDay).first()
    if not existing:
        plan = generate_38_day_plan()
        for day in plan:
            db.add(day)
        db.commit()

@router.get("")
def get_full_plan(db: Session = Depends(get_db)):
    ensure_plan_exists(db)
    return db.query(StudyPlanDay).order_by(StudyPlanDay.day_number).all()

@router.get("/today")
def get_today_plan(db: Session = Depends(get_db)):
    ensure_plan_exists(db)
    today = date.today().strftime("%Y-%m-%d")
    today_plan = db.query(StudyPlanDay).filter(StudyPlanDay.date == today).first()
    if today_plan:
        return today_plan
    all_plans = db.query(StudyPlanDay).order_by(StudyPlanDay.day_number).all()
    for plan in all_plans:
        if plan.date >= today:
            return plan
    return all_plans[-1] if all_plans else None

@router.get("/day/{day_number}")
def get_day_plan(day_number: int, db: Session = Depends(get_db)):
    ensure_plan_exists(db)
    plan = db.query(StudyPlanDay).filter(StudyPlanDay.day_number == day_number).first()
    if not plan:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Day not found")
    return plan
