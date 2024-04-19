#!/usr/bin/env python3
"""Session class"""
import os
from datetime import datetime
from .session_auth import SessionAuth
from typing import Dict, Any


class SessionExpAuth(SessionAuth):
    """Session system"""

    user_id_by_session_id: Dict[str, Dict[str, Any]] = {}

    def __init__(self):
        """Start a timed session"""
        session_duration = os.getenv('SESSION_DURATION', None)
        if session_duration is None:
            self.session_duration = 0
        else:
            try:
                self.session_duration = int(session_duration)
            except Exception as error:
                self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a user session"""
        session_id = super().create_session(user_id)
        if user_id != self.user_id_for_session_id[session_id]:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id_session = self.user_id_by_session_id.get(session_id, None)
        if user_id_session is None:
            return None
        if self.session_duration <= 0:
            return user_id_session.get('user_id', None)
        user_session_created_at = user_id_session.get('created_at', None)
        if user_session_created_at is None:
            return None
        time_now = datetime.now()
        user_session_duration = user_session_created_at + self.session_duration
        if user_session_duration < time_now:
            return None
        return user_id_session.get('user_id', None)
