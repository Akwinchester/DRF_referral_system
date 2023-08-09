from typing import Optional
import time
from referral_system.models import UserProfile
import jwt
import datetime


import random
import string
from referral_system.services.utils import logger, get_current_time


# Создает нового пользователя или возвращает существующего по номеру телефона
def create_user(phone: str) -> UserProfile:
    try:
        user = UserProfile.objects.get(phone=phone)
        logger.info(f"({get_current_time()}) В БД найден пользователь: {user}")
    except UserProfile.DoesNotExist:
        user = UserProfile.objects.create(phone=phone, invite_code=generate_invite_code())
        logger.info(f"({get_current_time()}) В БД создан пользователь: {user}")

    return user


# Генерирует код подтверждения для пользователя
def generate_confirmation_code(user: UserProfile) -> str:
    length = 4
    digits = string.digits
    confirmation_code = ''.join(random.choices(digits, k=length))

    user.confirmation_code = confirmation_code
    user.save()
    logger.info(f"({get_current_time()}) Для пользователя:{user} сгенерирован confirmation_code:{confirmation_code}")

    return confirmation_code


# Имитирует отправку SMS с кодом подтверждения
def send_confirmation_code(confirmation_code):
    # имитация отправки кода
    logger.info(f"({get_current_time()}) Отправка confirmation_code:{confirmation_code}")
    time.sleep(1)


# Аутентифицирует пользователя по номеру телефона и коду подтверждения
def authenticate_user(phone: str, confirmation_code: str) -> Optional[UserProfile]:
    try:
        user = UserProfile.objects.get(phone=phone)
        if user.confirmation_code == confirmation_code:
            logger.info(f"({get_current_time()}) Пользователь аутентифицирован по номеру телефона:{phone} и коду подтверждения:{confirmation_code}")
            return user
    except UserProfile.DoesNotExist as e:
        logger.info(f"({get_current_time()}) Ошибка аутентификации пользователя с телефоном:{phone} по коду подтверждения:{confirmation_code}\n Ошибка:{e}")
        return None


# Возвращает пользователя по id или номеру телефона
def get_user(user_id: Optional[int] = None, phone: Optional[str] = None) -> Optional[UserProfile]:
    try:
        user = None
        if user_id:
            user = UserProfile.objects.get(id=user_id)
        elif phone:
            user = UserProfile.objects.get(phone=phone)
        return user

    except UserProfile.DoesNotExist as e:
        logger.info(f"({get_current_time()}) get_user\nОшибка:{e}")
        return None


# Генерирует JWT токен для пользователя
def generate_token(user: UserProfile) -> bytes:
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    logger.info(f"({get_current_time()}) Сгенерирован токен для пользовтеля:{user}\ntoken:{token}")
    return token


# Аутентификация запроса по JWT токену
def jwt_authentication(request) -> Optional[bool]:
    token = request.headers.get('Authorization')

    if not token:
        return None

    user = validate_jwt_token(token)  # вызов вспомогательной

    if user:
        request.user = user
        logger.info(f"({get_current_time()}) Пользователь:{user} авторизован по токену:{token}")
        return True

    return None


# Валидирует JWT токен и возвращает пользователя
def validate_jwt_token(token: str) -> Optional[UserProfile]:
    try:
        payload = jwt.decode(jwt=token, key='secret', algorithm='HS256')
        user = get_user(user_id=payload['user_id'])

        logger.info(f"({get_current_time()}) Успешная валидация токена:{token}")
    except (jwt.DecodeError, jwt.ExpiredSignature):
        return None

    if user:
        return user

    return None


# Генерирует пригласительный код
def generate_invite_code() -> str:
    length = 6

    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    invite_code = ''.join(random.sample(char_set * length, length))

    return invite_code
