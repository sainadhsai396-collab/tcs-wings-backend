from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, topics, study_plan, questions, progress, exams, ai_router

app = FastAPI(title="TCS Wings Data Engineering Prep API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(topics.router)
app.include_router(study_plan.router)
app.include_router(questions.router)
app.include_router(progress.router)
app.include_router(exams.router)
app.include_router(ai_router.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "TCS Wings Data Engineering Prep API", "version": "1.0.0"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}
