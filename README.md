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

# 🔧 Deployment Challenges & Learnings

During deployment, several real-world backend issues were encountered and resolved:

🗄️ Database Connectivity Issues
Incorrect PostgreSQL connection string caused authentication failures
Resolved by properly configuring:
postgresql+psycopg2 driver
sslmode=require
Correct credentials from Neon

🧩 Table Creation Issues (SQLAlchemy)
Tables were not created initially
Root cause: models were not imported before Base.metadata.create_all()
Fix: explicitly imported all models during application startup

🌍 Environment Differences
Application worked locally with SQLite but failed in production with PostgreSQL
Required handling database-specific configurations and connection settings

🔐 Dependency Conflicts
Password hashing failed due to bcrypt/passlib incompatibility

Resolved by pinning versions:

passlib[bcrypt]==1.7.4
bcrypt==4.0.1

⚠️ Silent Failures
Exception handling during startup masked critical errors
Fixed by allowing errors to surface during deployment for proper debugging

# 🚀 4. Push to GitHub

```bash id="git1"
git add .
git commit -m "final project"
git push

## ⚙️ Setup

```bash
uvicorn src.main:app --reload