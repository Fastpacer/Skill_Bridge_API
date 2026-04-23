from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_signup():
    response = client.post("/auth/signup", json={
        "name": "test_user",
        "email": "test_user@test.com",
        "password": "1234",
        "role": "trainer"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login():
    client.post("/auth/signup", json={
        "name": "login_user",
        "email": "login_user@test.com",
        "password": "1234",
        "role": "trainer"
    })

    response = client.post("/auth/login", json={
        "email": "login_user@test.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_session():
    signup = client.post("/auth/signup", json={
        "name": "trainer_user",
        "email": "trainer_user@test.com",
        "password": "1234",
        "role": "trainer"
    })
    token = signup.json()["access_token"]

    response = client.post(
        "/sessions/?title=TestSession",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_attendance_student():
    signup = client.post("/auth/signup", json={
        "name": "student_user",
        "email": "student_user@test.com",
        "password": "1234",
        "role": "student"
    })
    token = signup.json()["access_token"]

    response = client.post(
        "/attendance/mark?session_id=1&status=present",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_monitoring_token():
    signup = client.post("/auth/signup", json={
        "name": "monitor_user",
        "email": "monitor_user@test.com",
        "password": "1234",
        "role": "monitoring_officer"
    })
    token = signup.json()["access_token"]

    response = client.post(
        "/auth/monitoring-token",
        json={"key": "skillbridge_monitor_123"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "monitoring_token" in response.json()