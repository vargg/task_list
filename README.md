# API сервис для ведения списка задач.

http://178.154.229.5/

## Стэк
[Python](https://www.python.org/) v.3.9, [Django](https://www.djangoproject.com/) v.3.2.6, [Django REST framework](https://www.django-rest-framework.org/) v.3.12.4, [nginx](https://nginx.org/en/docs/) v.1.19.3, [PostgreSQL](https://www.postgresql.org) v.12.4, [Docker](https://www.docker.com/) v.20.10.8.

## Описание.
Сервис для ведения списка задач. Регистрация пользователей по логину и паролю с последующим поступом по JWT-токеную. Имеется возможность добавления/изменения/удаления задач (пользователь может изменять и удалять только свои задачи); просмотр задачи или списка задач.

## API.
Подробная информация по работе с API доступна на странице `swagger/`.

### Пример запроса:
- получение токена по логину и паролю

request `users/token/ [POST]`
```json
{
  "username": "str",
  "password": "str"
}
```
response
```json
{
  "refresh": "str",
  "access": "str"
}
```

последующие запросы выполнять с заголовком `Authorization: Token access_token` (вместо "access_token" указать полученный токен "access").

- создание новой задачи:


  request `tasks/ [POST]`
```json
{
  "name": "str",
  "description": "str",
  "deadline": "dd.mm.yyyy",
  "performers": [user_id, user_id]
}
```
response
```json
{
    "id": int,
    "author": {
        "id": int,
        "username": "str",
        "full_name": "str"
    },
    "performers": [
      {
        "id": int,
        "username": "str",
        "full_name": "str"
      },
      {
        "id": int,
        "username": "str",
        "full_name": "str"
      },
    ],
    "name": "str",
    "description": "str",
    "deadline": "dd.mm.yyyy",
    "attachment": "http://...*"
}
```

## Установка и запуск.
Для запуска требуются [docker](https://docs.docker.com/get-docker/) и [docker compose](https://docs.docker.com/compose/install/).
Клонировать репозиторий:
```shell
git clone https://github.com/vargg/task_list.git
```
В корневом каталоге проекта создать файл `.env` в котором должны быть заданы следующие переменные:
```
-DB_NAME
-DB_ENGINE
-DB_USER
-DB_PASSWORD
-POSTGRES_PASSWORD
-DB_HOST
-DB_PORT
-DJANGO_SECRET_KEY
```
Запуск контейнеров:
```shell
docker-compose up
```
Сервис будет доступен по ссылке [http://localhost](http://localhost).

Применение миграций:
```shell
docker-compose exec -T backend python manage.py migrate
```
Для сбора статики:
```shell
docker-compose exec -T backend python manage.py collectstatic --no-input
```
Остановка:
```shell
docker-compose down
```
