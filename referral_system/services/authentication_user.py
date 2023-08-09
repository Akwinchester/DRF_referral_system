# auth_service.py
import time
from referral_system.models import UserProfile
from ..utils import generate_invite_code

import random
import string


def create_user(phone):
    try:
        user = UserProfile.objects.get(phone=phone)
    except UserProfile.DoesNotExist:
        user = UserProfile.objects.create(phone=phone, invite_code=generate_invite_code())
    print(user)

    return user


def generate_confirmation_code(user):
    length = 4
    digits = string.digits
    confirmation_code = ''.join(random.choices(digits, k=length))

    user.confirmation_code = confirmation_code
    user.save()

    return confirmation_code


def send_confirmation_code():
    # имитация отправки кода
    time.sleep(1)


def authenticate_user(phone, code):
    try:
        user = UserProfile.objects.get(phone=phone)
        if user.confirmation_code == code:
            return user
    except UserProfile.DoesNotExist:
        return None


def get_user(user_id=None, phone=None):
    try:
        user = None
        if user_id:
            user = UserProfile.objects.get(id=user_id)
        elif phone:
            user = UserProfile.objects.get(phone=phone)
        return user

    except UserProfile.DoesNotExist:
        return None
