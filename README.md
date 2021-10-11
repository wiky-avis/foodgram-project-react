# Foodgram

![example workflow](https://github.com/wiky-avis/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Ip-адрес сервера, на котором запущено приложение [62.84.121.227](http://62.84.121.227/recipes)

## Стек: 
Python 3, Django 3, Django REST Framework, Docker, PostgreSQL, Simple-JWT, Joser.

## Описание:
Проект Foodgram позволяет постить рецепты, делиться и скачивать списки продуктов

Документация к API доступна по адресу http://localhost/api/docs/

## Алгоритм регистрации пользователей:
Регистрация проходит на сайте, по форме регистрации

## Установка
Для работы приложения требуется установка на ваш компьютер [Python](https://www.python.org/downloads/), [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-windows), [PostgreSQL](https://postgrespro.ru/windows).

Склонируйте репозиторий на локальную машину:

  `git clone https://github.com/wiky-avis/foodgram-project-react.git`

В папке backend необходимо создать файл .env и заполнить переменные окружения.

Запустите docker-compose:

  `make build`

Применените миграции базы данных:

  `make migrate`

Сбор статических файлов:

  `make static`
  
Проект запущен и доступен по адресу [http://localhost/](http://localhost/).

Создаем суперпользователя:

  `make createsuperuser`

Заполнения базы начальными данными:

  `make loaddata`

Остановить все запущенные контейнеры:

  `docker-compose down`


### Вход на сайт/в админку:

```
admin@admin.ru
admin
```
