# utils.py
from .models.models import UserProfile
import random
import string
import jwt
import datetime


def authenticate_user(phone, code):
  try:
    user = UserProfile.objects.get(phone=phone)
    if user.confirmation_code == code:
      return user
  except UserProfile.DoesNotExist:
    return None


def generate_invite_code():
    length = 6

    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    invite_code = ''.join(random.sample(char_set * length, length))

    return invite_code


def generate_code():
    length = 4
    digits = string.digits
    code = ''.join(random.choices(digits, k=length))
    return code


def check_code(user, code):
    if user.confirmation_code == code:
        return True
    return False
