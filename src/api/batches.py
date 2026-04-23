from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from src.db import get_db
from src.models.models import Batch, BatchInvite
from src.utils.auth import require_role

router = APIRouter(prefix="/batches")


# Trainer creates batch
@router.post("/")
def create_batch(name: str, db: Session = Depends(get_db), user=Depends(require_role("trainer"))):
    batch = Batch(name=name)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


# Generate invite token
@router.post("/{batch_id}/invite")
def generate_invite(batch_id: int, db: Session = Depends(get_db), user=Depends(require_role("trainer"))):
    token = str(uuid.uuid4())

    invite = BatchInvite(
        batch_id=batch_id,
        token=token
    )

    db.add(invite)
    db.commit()

    return {"invite_token": token}


# Student joins batch
@router.post("/join")
def join_batch(token: str, db: Session = Depends(get_db), user=Depends(require_role("student"))):
    invite = db.query(BatchInvite).filter(BatchInvite.token == token).first()

    if not invite or invite.used:
        raise HTTPException(status_code=400, detail="Invalid token")

    invite.used = True
    db.commit()

    return {"msg": "Joined batch"}