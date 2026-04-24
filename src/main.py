from fastapi import FastAPI
from src.db import Base, engine

# 🔥 IMPORTANT: import ALL models so SQLAlchemy registers them
from src.models.models import User, Session, Attendance, Batch, BatchInvite

from src.api import auth, sessions, attendance, batches, monitoring

app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("🚀 APP STARTING...")
    try:
        # Debug: confirm tables detected
        print("TABLES DETECTED:", Base.metadata.tables.keys())

        Base.metadata.create_all(bind=engine)

        print("✅ TABLES CREATED SUCCESSFULLY")
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