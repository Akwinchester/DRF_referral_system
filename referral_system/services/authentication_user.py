# auth_service.py
import time
from referral_system.models import UserProfile
import jwt
import datetime


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


def generate_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def jwt_authentication(request):
    token = request.headers.get('Authorization')

    if not token:
        return None

    user = validate_jwt_token(token)  # вызов вспомогательной

    if user:
        request.user = user
        return True

    return None


def validate_jwt_token(token):
    try:
        print(token)
        payload = jwt.decode(jwt=token, key='secret', algorithm='HS256')
        print(payload)
    except jwt.ExpiredSignature:
        return None

    user = get_user(user_id=payload['user_id'])

    if user:
        return user

    return None


def generate_invite_code():
    length = 6

    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    invite_code = ''.join(random.sample(char_set * length, length))

    return invite_code
