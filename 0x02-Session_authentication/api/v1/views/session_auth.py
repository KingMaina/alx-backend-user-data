#!/usr/bin/env python3
""" Module of Session views
"""
import os
from typing import List
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST /api/v1/auth_session_login
    Return:
      - user object
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email == '' or email is None:
        return jsonify({"error": "email missing"}), 400
    if password == '' or password is None:
        return jsonify({"error": "password missing"}), 400
    user: List[User] = User.search({'email': email})
    if not user or not len(user):
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    cookie_name = os.getenv('SESSION_NAME')
    response = jsonify(user[0].to_json())
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_session():
    """Logout the user session"""
    from api.v1.app import auth

    is_logout_valid = auth.destroy_session(request)
    if is_logout_valid is False:
        abort(404)
    return jsonify({}), 200
