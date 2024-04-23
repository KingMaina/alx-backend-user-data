#!/usr/bin/env python3
"""Integration tests for the authentication system"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
API_URL='http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Register a user"""
    payload = dict(email=email, password=password)
    expected_success = {"email": email, "message": "user created"}
    expected_fail = {"email": "email already registered"}

    # Register user first time should be successful
    response = requests.post('{}/'.format(API_URL), payload)
    assert response.status_code == 200
    assert response.json() == expected_success

    # Register user second time should fail
    response = requests.post('{}/'.format(API_URL), payload)
    assert response.status_code == 400
    assert response.json() == expected_fail


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)