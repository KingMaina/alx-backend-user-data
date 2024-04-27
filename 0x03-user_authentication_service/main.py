#!/usr/bin/env python3
"""Integration tests for the authentication system"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
API_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Register a user"""
    payload = dict(email=email, password=password)
    expected_success = {"email": email, "message": "user created"}
    expected_fail = {"message": "email already registered"}
    try:
        response = requests.post('{}/users'.format(API_URL), payload)
        assert response.status_code == 200
        assert response.json() == expected_success
    except AssertionError:
        # Registering an existing account should fail
        assert response.status_code == 400
        assert response.json() == expected_fail


def log_in_wrong_password(email: str, password: str) -> None:
    """Test user log in using incorrect password"""
    payload = dict(email=email, password=password)
    response = requests.post('{}/sessions'.format(API_URL), payload)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test user accessing profile page when not authenticated"""
    response = requests.get('{}/profile'.format(API_URL),
                            cookies={'session_id': None})
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Login a user"""
    payload = dict(email=email, password=password)
    response = requests.post('{}/sessions'.format(API_URL), payload)
    session_id = response.cookies.get("session_id", None)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


def profile_logged(session_id: str) -> None:
    """Test an authenticated user accessing profile page"""
    payload = dict(session_id=session_id)
    response = requests.get('{}/profile'.format(API_URL), cookies=payload)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Log out a user"""
    cookies = dict(session_id=session_id)
    response = requests.delete('{}/sessions'.format(API_URL),
                               cookies=cookies)
    assert response.status_code == 200  # index page
    assert response.url == '{}/'.format(API_URL)  # user redirected
    assert response.cookies.get('session_id', None) is None


def reset_password_token(email: str) -> str:
    """Test password reset token"""
    payload = dict(email=email)
    response = requests.post('{}/reset_password'.format(API_URL), payload)
    res_content = response.json()
    assert response.status_code == 200
    assert res_content.get('email') == email
    assert res_content.get('reset_token') is not None
    return res_content.get('reset_token', None)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test a user updating their password"""
    payload = dict(email=email,
                   reset_token=reset_token,
                   new_password=new_password)
    response = requests.put('{}/reset_password'.format(API_URL), payload)
    res_content = response.json()
    assert response.status_code == 200
    assert res_content == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
