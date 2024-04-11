#!/usr/bin/env python3

"""Contains functions that filter log data"""
import re
import logging
import os
from typing import List
import mysql.connector

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filters log data to obfuscate sensitive fields"""
    return ''.join(f'{field}={redaction}{separator}'
                   for field in fields)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize a formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats data"""
        return filter_datum(fields=self._fields, redaction=self.REDACTION,
                            message=super().format(record),
                            separator=self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler(None)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to the database and returns the connector"""
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    config = {
        'host': db_host,
        'user': db_username,
        'password': db_password,
        'database': db_name,
    }
    return mysql.connector.connect(**config)


def main() -> None:
    """Initializes the database and retrieves filtered out information"""
    db_connection = get_db()
    # Define PII to obfuscate
    pii = ('name', 'email', 'phone', 'ssn', 'password')
    # Get all users
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT * FROM users;')
    # Get the column names used tocreate log messages
    columns = list(db_cursor.column_names)
    for row in db_cursor:
        obfuscated_data = ''.join('{}={};'.format(columns[index], data)
                                  for index, data in enumerate(row))
        log_record = logging.LogRecord(None, logging.INFO, None,
                                       None, obfuscated_data, None, None)
        formatter = RedactingFormatter(fields=list(pii))
        print(formatter.format(log_record))
    db_cursor.close()
    db_connection.close()


if __name__ == '__main__':
    main()
