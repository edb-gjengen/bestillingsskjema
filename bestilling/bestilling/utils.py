import re

def is_phone_valid(phone_str):
    pattern = re.compile('^(\+\d{2,4})?\s*(\s?\d){6,}$')
    return pattern.match(phone_str) is not None

def is_email_valid(email_str):
    pattern = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')
    return pattern.match(email_str) is not None
