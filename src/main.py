from fastapi import FastAPI
from src.db import Base, engine

# VERY IMPORTANT — force model import
from src.models.models import User, Session, Attendance

from src.api import auth, sessions, attendance, batches, monitoring

app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("🚀 APP STARTING...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ TABLES CREATED")
    except Exception as e:
        print("❌ DB INIT FAILED:", e)


app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(batches.router)
app.include_router(monitoring.router)


@app.get("/")
def root():
    return {"msg": "SkillBridge API running"}