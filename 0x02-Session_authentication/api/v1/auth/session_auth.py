#!/usr/bin/env python3
"""Session class"""
from uuid import uuid4
from models.user import User
from .auth import Auth
from typing import Dict


class SessionAuth(Auth):
    """Session system"""

    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a user session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Returns the current user in the session"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        if user:
            return user

    def destroy_session(self, request=None):
        """Destroys a user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
