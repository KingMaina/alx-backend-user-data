#!/usr/bin/env python3

"""Contains excrypting functions"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """Hashes, salts and returns a password"""
    return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password matches a hashed password"""
    pass_bytes: ByteString = bytes(password, encoding='utf-8')
    if bcrypt.checkpw(password, hashed_password):
        return True
    else:
        return False
