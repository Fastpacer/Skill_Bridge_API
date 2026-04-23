from pydantic import BaseModel


class Signup(BaseModel):
    name: str
    email: str
    password: str
    role: str


class Login(BaseModel):
    email: str
    password: str

class MonitoringRequest(BaseModel):
    key: str