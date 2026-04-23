
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import get_db
from src.models.models import Session as SessionModel
from src.utils.auth import require_role

router = APIRouter(prefix="/sessions")


@router.post("/")
def create_session(title: str, db: Session = Depends(get_db), user=Depends(require_role("trainer"))):
    session = SessionModel(title=title, trainer_id=user["user_id"])
    db.add(session)
    db.commit()
    db.refresh(session)
    return session