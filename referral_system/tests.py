import pytest
from django.urls import reverse
from rest_framework.test import APIClient


from referral_system.services.authentication_user import (
    create_user,
    generate_confirmation_code,
    authenticate_user,
    generate_token
)
from referral_system.services.utils import logger


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {'phone': '+79001231234'}


# Тест регистрации нового пользователя
# Проверяет, что запрос на регистрацию возвращает 200 и данные с confirmation_code
@pytest.mark.django_db
def test_register_user(api_client, user_data):
    phone = user_data['phone']

    url = reverse('phone_auth')
    rsp = api_client.post(url, data={'phone': phone})

    user_data.update(rsp.data)

    assert rsp.status_code == 200
    assert rsp.data['confirmation_code'] != None


# Тест авторизации существующего пользователя
# Проверяет, что при отправке верных данных возвращается 200
@pytest.mark.django_db
def test_auth_existing_user(api_client, user_data):
    phone = user_data['phone']

    user = create_user(phone)
    confirmation_code = generate_confirmation_code(user)

    url = reverse('phone_auth')
    rsp = api_client.post(url, data={
        'phone': phone,
        'confirmation_code': confirmation_code
    })

    assert rsp.status_code == 200


# Тест проверки кода подтверждения
# Проверяет, что при отправке верного кода возвращается 200 и токен
@pytest.mark.django_db
def test_verify_code(api_client, user_data):
    phone = user_data['phone']

    user = create_user(phone)
    confirmation_code = generate_confirmation_code(user)

    url = reverse('verify_code')
    rsp = api_client.post(url, data={
        'phone': phone,
        'confirmation_code': confirmation_code
    })

    assert rsp.status_code == 200
    assert 'token' in rsp.data


# Тест получения профиля пользователя
# Проверяет, что при отправке токена возвращается 200 и данные профиля
@pytest.mark.django_db
def test_user_profile(api_client, user_data):
    user = create_user(phone=user_data['phone'])
    confirmation_code = generate_confirmation_code(user)
    authenticate_user(user_data['phone'], confirmation_code)
    token = generate_token(user)

    url = reverse('user_profile')
    logger.info(f"{api_client.headers}")
    rsp = api_client.get(url, headers={'Authorization': token})

    assert rsp.status_code == 200
    assert rsp.data['phone'] == user_data['phone']
    assert rsp.data['referred_users'] == []


# Тест добавления реферала
# Проверяет, что реферал успешно добавляется в список пользователя
@pytest.mark.django_db
def test_add_referral(api_client):
    phone_1 = '+79001231234'
    phone_2 = '+79001254797'

    user_1 = create_user(phone=phone_1)
    confirmation_code = generate_confirmation_code(user_1)
    authenticate_user(phone_1, confirmation_code)

    user_2 = create_user(phone=phone_2)

    token_2 = generate_token(user_2)

    url = reverse('referral_add')
    rsp = api_client.post(url,
                          headers={'Authorization': token_2},
                          data={'invite_code': user_1.invite_code}
                          )

    assert rsp.status_code == 200

    user_1.refresh_from_db()
    assert len(user_1.referred_users.all()) == 1
