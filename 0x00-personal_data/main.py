#!/usr/bin/env python3
"""
Main file
"""
import logging
import re
import csv


hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid
filter_datum = __import__('filtered_logger').filter_datum
get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS
get_db = __import__('filtered_logger').get_db


fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))


# ## Task 1

# RedactingFormatter = __import__('filtered_logger').RedactingFormatter

# message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
# log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
# formatter = RedactingFormatter(fields=("email", "ssn", "password"))
# print(formatter.format(log_record))



# print(get_logger.__annotations__.get('return'))
# print("PII_FIELDS: {}".format(len(PII_FIELDS)))

# with open('user_data.csv') as user_data:
#     reader = csv.reader(user_data)
#     new_data = ''
#     fields = []
#     count = 0
#     for row in reader:
#         if count == 0:
#            fields = row[:]
#         else:
#             new_data = ''.join('{}={};'.format(fields[index],data)
#                                for index, data in enumerate(row))
#             print(filter_datum(fields=PII_FIELDS, redaction="???", message=new_data, separator=';'))
#         count += 1

# # Task 3
# db = get_db()
# cursor = db.cursor()
# cursor.execute("SELECT COUNT(*) FROM users;")
# for row in cursor:
#     print(row[0])
# cursor.close()
# db.close()


# password = "MyAmazingPassw0rd"
# print(hash_password(password))
# print(hash_password(password))


# password = "MyAmazingPassw0rd"
# encrypted_password = hash_password(password)
# print(encrypted_password)
# print(is_valid(encrypted_password, password))

