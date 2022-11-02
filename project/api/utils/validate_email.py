import re

from jsonschema import ValidationError

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def regex_email(email):
    if re.match(regex, email):
        return True
    return False
