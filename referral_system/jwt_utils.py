import jwt
import datetime

from referral_system.services.authentication_user import get_user


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
