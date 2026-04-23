from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db import get_db
from src.models.models import User
from src.schemas.auth import MonitoringRequest
from src.utils.auth import get_current_user, create_monitoring_token
from src.config import settings
from src.schemas.auth import Signup, Login
from src.utils.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(data: Signup, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email exists")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({"user_id": user.id, "role": user.role})
    return {"access_token": token}


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):    
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id, "role": user.role})
    return {"access_token": token}

@router.post("/monitoring-token")
def get_monitoring_token(
    data: MonitoringRequest,
    user=Depends(get_current_user)
):
    # Check role
    if user["role"] != "monitoring_officer":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Check API key
    if data.key != settings.MONITORING_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    token = create_monitoring_token({
        "user_id": user["user_id"],
        "role": user["role"]
    })

    return {"monitoring_token": token}