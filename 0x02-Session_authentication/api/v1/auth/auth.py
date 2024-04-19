#!/usr/bin/env python3
"""Authentication class"""
import os
from flask import request
from typing import TypeVar, List
import re


class Auth:
    """Auth system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authorization?"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) <= 0:
            return True
        if path[-1] != '/':
            path += '/'
        for _path in excluded_paths:
            if re.match(_path, path) is not None:
                return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """Auth headers"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user"""
        return None

    def session_cookie(self, request=None):
        """Returns the cookie from a request"""
        if request is None:
            return None
        session_name: str = os.getenv('SESSION_NAME', None)
        return request.cookies.get(session_name, None)
