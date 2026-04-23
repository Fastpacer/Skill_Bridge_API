from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import get_db
from src.models.models import Attendance
from src.utils.auth import require_role

router = APIRouter(prefix="/attendance")


@router.post("/mark")
def mark_attendance(session_id: int, status: str, db: Session = Depends(get_db), user=Depends(require_role("student"))):
    record = Attendance(
        session_id=session_id,
        student_id=user["user_id"],
        status=status
    )
    db.add(record)
    db.commit()
    return {"msg": "Attendance marked"}


# Trainer views attendance
@router.get("/{session_id}")
def get_attendance(session_id: int, db: Session = Depends(get_db), user=Depends(require_role("trainer"))):
    records = db.query(Attendance).filter(Attendance.session_id == session_id).all()
    return records