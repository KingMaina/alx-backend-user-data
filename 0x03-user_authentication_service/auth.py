#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from typing import Union
from uuid import uuid4
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Encrypts a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique ID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self) -> None:
        """Initializs the Auth system"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials"""
        user = self._db.find_user_by(email=email)
        if user is None:
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Creates a new user session"""
        user = self._db.find_user_by(email=email)
        if user is not None:
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get the user from a session"""
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id=session_id)
        if user is None:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroys a user session"""
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token"""
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        reset_token = str(uuid4())
        self._db.update_user(user_id=user.id,
                             reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password"""
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError
        hashed_password = _hash_password(password.encode())
        self._db.update_user(user_id=user.id, hashed_password=hashed_password,
                             reset_token=None)
