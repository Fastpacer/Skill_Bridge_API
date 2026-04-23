from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Swagger-compatible security
security = HTTPBearer()


# -----------------------------
# PASSWORD FUNCTIONS
# -----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# -----------------------------
# TOKEN CREATION
# -----------------------------
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_monitoring_token(data: dict):
    payload = data.copy()
    payload["scope"] = "monitoring"
    payload["exp"] = datetime.utcnow() + timedelta(hours=1)  # short-lived
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# -----------------------------
# TOKEN DECODE
# -----------------------------
def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# CURRENT USER
# -----------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    print("RAW CREDENTIALS:", credentials)

    if not credentials:
        raise HTTPException(status_code=401, detail="No credentials")

    token = credentials.credentials
    print("TOKEN RECEIVED:", token)

    return decode_token(token)


# -----------------------------
# ROLE-BASED ACCESS
# -----------------------------
def require_role(role: str):
    def checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return checker


# -----------------------------
# MONITORING TOKEN CHECK
# -----------------------------
def require_monitoring_scope(user=Depends(get_current_user)):
    if user.get("scope") != "monitoring":
        raise HTTPException(status_code=401, detail="Invalid monitoring token")
    return user