# api_yatube

Проект реализует полноценный API для проекта YAMDB.

Для полного доступа к API с возможностьюу добавлять посты и комментарии,
редактировать свои посты и комментарии, а также подписываться
на других пользователей необходимо получить JWT-токен.

## Установка и настройка

1. Клонируйте репозиторий:

```bash
git clone git@github.com:theartemio/api_yamdb.git
```

2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

4. Выполните миграции:

```bash
python manage.py migrate
```

5. При необходимости загрузите базу данных из .csv файлов с помощью команды:

```bash
python manage.py import_csv
```

## Использование

### Регистрация пользователя

POST api/v1/auth/signup/ — передайте эмейл и юзернейм, чтобы зарегистрироваться.
Пример запроса:

```json
{
  "email": "user@example.com",
  "username": "string",
}
```

### Аутентификация и получение JWT-токена

POST api/v1/auth/token/ — передайте юзернейм и полученный код подтверждения, чтобы получить токен.
Пример запроса:

```json
{
    "username": "User",
    "confirmation_code": 0000
}
```

### Основные эндпоинты

- POST /api/v1/auth/signup/ — зарегистрироваться.
- POST /api/v1/auth/token/ — получить и обновить JWT-токен.
- GET /api/v1/titles/ — просмотреть базу данных произведений. Доступны фильтры.
- GET /api/v1/categories/ — просмотреть категории.
- GET /api/v1/genres/ — просмотреть жанры.
- GET /api/v1/titles/pk/reviews/ — просмотреть рецензии на произведение.
- POST /api/v1/titles/pk/reviews/ — добавить свою рецензию на произведение.
- GET /api/v1/reviews/{post_id}/comments/ — получить комментарии к рецензии.
- POST /api/v1/reviews/{post_id}/comments/ — добавить новый комментарий.
- GET /api/v1/reviews/{post_id}/comments/{comment_id}/ — получить информацию о комментарии.
- PUT /api/v1/reviews/{post_id}/comments/{comment_id}/ — обновить комментарий.
- DELETE /api/v1/reviews/{post_id}/comments/{comment_id}/ — удалить комментарий.
- GET /api/v1/users/me/ — информация о своем аккаунте.

Более подробное описание находится по адресу http://127.0.0.1:8000/redoc.


## Требования
- Python 3.8+
- Django 3.2+
- Djangorestframework 3.12+

## Авторы

**Основной функционал проекта**
Артемий Третьяков [GitHub](https://github.com/theartemio)
Владислав Смыслов [GitHub](https://github.com/VladSmyslov)
Абдул Малик [GitHub](https://github.com/Abdul-Malik-2005/)

**Исходный репозиторий**
Яндекс.Практикум [GitHub](https://github.com/yandex-praktikum/).

## Лицензия
Этот проект распространяется на условиях лицензии MIT.
