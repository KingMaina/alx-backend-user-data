#!/usr/bin/env python3
"""Basic Flask API"""
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    request
)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Entry point of API"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Registers a user"""
    try:
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as error:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login a user"""
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    is_auth_valid = AUTH.valid_login(email, password)
    if not is_auth_valid:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Logout a user's session"""
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Get the user profile"""
    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    email = request.form.get('email', None)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError as error:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Updates the user's password"""
    email = request.form.get('email', None)
    reset_token = request.form.get('reset_token', None)
    new_password = request.form.get('new_password', None)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except Exception as error:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
