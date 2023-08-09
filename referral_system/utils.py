# utils.py
import random
import string


def generate_invite_code():
    length = 6

    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    invite_code = ''.join(random.sample(char_set * length, length))

    return invite_code


def check_code(user, code):
    if user.confirmation_code == code:
        return True
    return False
