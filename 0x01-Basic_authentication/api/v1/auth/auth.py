#!/usr/bin/env python3
"""Authentication class"""
from typing import TypeVar, List
from flask import request


class Auth:
    """Auth system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authorization?"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) <= 0:
            return True
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Auth headers"""
        if request is None:
            return None
        return request.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user"""
        return None
