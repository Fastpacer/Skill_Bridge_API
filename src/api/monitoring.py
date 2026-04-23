from fastapi import APIRouter, Depends, HTTPException
from src.utils.auth import get_current_user

router = APIRouter(prefix="/monitoring")


def require_monitoring_scope(user=Depends(get_current_user)):
    if user.get("scope") != "monitoring":
        raise HTTPException(status_code=401, detail="Invalid monitoring token")
    return user


@router.get("/attendance")
def monitoring_attendance(user=Depends(require_monitoring_scope)):
    return {"msg": "Monitoring data access granted"}