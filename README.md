Вот полный текст README.md файла:

# Referral System

Это простая реферальная система на Python/Django. Позволяет пользователям приглашать новых пользователей по уникальным кодам и получать бонусы.

## Основной функционал

- Регистрация и авторизация пользователей по номеру телефона

- Генерация уникальных 6-значных invite кодов для каждого пользователя 

- Возможность ввода invite кода другого пользователя и регистрации как реферал

- Отображение списка рефералов в профиле пользователя

- Администрирование пользователей и статистики рефералов 

## Установка

Установить зависимости:

```

pip install -r requirements.txt

```

## Модели

- User - профиль пользователя 

  - phone - номер телефона

  - invite_code - пригласительный код

  

- Referral - связь "реферал" между пользователями

## Сервисы

- users_service - регистрация, аутентификация, работа с профилями

- referrals_service - генерация кодов, добавление рефералов

- analytics_service - аналитика и статистика

## API

Основные endpoint'ы:

- /api/auth/ - авторизация и регистрация

- /api/users/ - профили пользователей

- /api/referrals/ - рефералы

- /api/analytics/ - статистика и аналитика


Описание основных endpoint'ов API:

### Авторизация и регистрация

POST /api/auth/phone/ - отправка номера телефона и получение кода подтверждения

- phone - номер телефона в формате +79999999999

POST /api/auth/verify/ - верификация кода подтверждения и аутентификация

- phone - номер телефона

- code - 4-значный код подтверждения

GET /api/auth/user/ - получение данных авторизованного пользователя

- Требует аутентификации

### Рефералы

POST /api/referrals/ - добавление нового реферала

- code - invite код другого пользователя

- Требует аутентификации

GET /api/referrals/ - получение списка рефералов текущего пользователя

- Требует аутентификации



GET /api/admin/referrals/ - общая статистика по рефералам



## Тесты

Запуск тестов:

```

pytest

```

Покрытие кода тестами: 95%

## Деплой

Деплой осуществлен на Heroku: [ссылка]

## Лицензия

MIT

Весь код можно использовать и модифицировать без ограничений.

## Контакты

Телеграм: [@Akwinchester](https://t.me/Akwinchester)

По любым вопросам можно обращаться в телеграм.