#!/usr/bin/env python3
"""Session Authenticatioon with persistence"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session Authenitication with database storage"""

    def create_session(self, user_id: str = None) -> str:
        """Creates a user session"""
        super().create_session(user_id)
        user_sess = UserSession()
        return user_sess.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user based on a Session ID"""
        super().user_id_for_session_id(session_id)
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id_session = UserSession.search({'session_id', session_id})
        if user_id_session is None:
            return None
        return user_id_session[0].get('user_id')

    def destroy_session(self, request=None):
        """Destroys a user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user = UserSession.search({'session_id': session_id})
        if user is None:
            return False
        UserSession.remove()
        return True
