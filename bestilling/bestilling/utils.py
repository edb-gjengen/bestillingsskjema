import re
from django.core.exceptions import ValidationError
from django.conf import settings


def is_phone_valid(phone_str):
    pattern = re.compile('^(\+\d{2,4})?\s*(\s?\d){6,}$')
    return pattern.match(phone_str) is not None and len(phone_str) <= 20


def is_email_valid(email_str):
    pattern = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')
    return pattern.match(email_str) is not None and len(email_str) <= 50


def validate_file_extension(value):
    if hasattr(settings, 'UPLOAD_FILENAME_EXTENSIONS_ALLOWED')\
            and type(settings.UPLOAD_FILENAME_EXTENSIONS_ALLOWED) == list:
        for ext in settings.UPLOAD_FILENAME_EXTENSIONS_ALLOWED:
            if value.name.lower().endswith(ext):
                return  # bail out
        raise ValidationError(u'Ikke tillatt filendelse i "{0}"'.format(value))