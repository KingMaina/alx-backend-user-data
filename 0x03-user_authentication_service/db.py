#!/usr/bin/env python3
"""DB module
"""
from typing import Mapping
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB():
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user based on user properties"""
        user_keys = ('id', 'email', 'hashed_password',
                     'session_id', 'reset_token')
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        results = self._session.query(User).filter_by(**kwargs).first()
        if results is None:
            raise NoResultFound
        return results

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user"""
        if not kwargs:
            raise ValueError
        self.find_user_by(id=user_id)
        user_keys = ('id', 'email', 'hashed_password',
                        'session_id', 'reset_token')
        for key in kwargs.keys():
            if key not in user_keys:
                raise ValueError
        self._session.query(User).update(kwargs)
        self._session.commit()
