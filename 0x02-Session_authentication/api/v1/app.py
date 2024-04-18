#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, session
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = os.getenv('AUTH_TYPE')
if auth_type is not None:
    if auth_type == 'basic_auth':
        from .auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == 'session_auth':
        from .auth.session_auth import SessionAuth
        auth = SessionAuth()
    else:
        from .auth.auth import Auth
        auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """Unauthorized error handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Forbidden error handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def validate_request():
    """Validates if a request is allowed to access the API"""
    excluded_routes = ['/api/v1/status/',
                       '/api/v1/unauthorized/',
                       '/api/v1/forbidden/',
                       '/api/v1/auth_session/login/']
    if auth:
        if auth.require_auth(request.path, excluded_routes):
            auth_token = auth.authorization_header(request)
            session_auth = auth.session_cookie(request)
            if auth_token is None and session_auth is None:
                abort(401)
            user = auth.current_user(request)
            if user is None:
                abort(403)
            else:
                request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
