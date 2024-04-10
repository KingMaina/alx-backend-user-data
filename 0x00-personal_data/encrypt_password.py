#!/usr/bin/env python3

"""Contains excrypting functions"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes, salts and returns a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password matches a hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
