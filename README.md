# SkillBridge API

A backend system for managing training sessions, attendance, and monitoring access with role-based authentication.

## 🚀 Features

- JWT Authentication (Signup/Login)
- Role-Based Access Control (Trainer, Student, Monitoring Officer)
- Session & Attendance Management
- Batch & Invite System
- Monitoring Officer Dual Token System (API key + scoped JWT)
- FastAPI + SQLAlchemy backend
- Pytest test coverage

---

## 🧠 Architecture Highlights

- Modular FastAPI structure
- JWT-based auth with role validation
- Secondary scoped token for monitoring endpoints
- Clean separation of concerns (api, models, utils)

---

## 🔐 Authentication Flow

1. User signs up & logs in → receives access token
2. Monitoring officer requests monitoring token using:
   - access token
   - API key
3. Monitoring endpoints require monitoring token

---

---

# 🚀 4. Push to GitHub

```bash id="git1"
git add .
git commit -m "final project"
git push

## ⚙️ Setup

```bash
uvicorn src.main:app --reload