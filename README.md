# api_yamdb
api_yamdb


## Описание
Проект YaMDb позволяет собирать отзывы пользователей на произведения, ставить оценку произведению и и оставлять комментарии к отзывам.


## Установка
1. Склонировать репозиторий:
    '''
    git clone git@github.com:username/api_yamdb.git
    '''
2. Установить и активировать виртуальное окружение:
    '''
    python3 -m venv venv

    #для OS Linux и MacOS
    source venv/Scripts/activate

    #для OS Windows
    source venv/Scripts/activate
    '''
3. Установить зависимости:
    '''
    pip install -r requirements.txt
    '''
4. Выполнить миграции:
     ```
    python3 manage.py makemigrations
    python manage.py migrate
    ```
5. Запустить сервер:
    ```
    python manage.py runserver
    ```


## Примеры запросов:
    Регистрация нового пользователя
    POST /auth/signup/
    Content-Type: application/json

    {
        "email": "user@example.com",
        "username": "^w\\Z"
    }

    Ответ:

    {
        "email": "string",
        "username": "string"
    }


    Получение списка всех жанров
    GET /genres/
    Content-Type: application/json

    Ответ:

    {

        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "^-$"
            }
        ]
    }



    Добавление нового отзыва
    POST /titles/{title_id}/reviews/
    Content-Type: application/json

    {
        "text": "string",
        "score": 1
    }

    Ответ:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }