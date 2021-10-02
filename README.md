# Foodgram

![example workflow](https://github.com/wiky-avis/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Ip-адрес сервера, на котором запущено приложение [84.252.138.212](http://84.252.138.212/)

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

Запустите docker-compose:

  `docker-compose up -d`

Создайте и применените миграции базы данных:

  `docker-compose exec backend python manage.py makemigrations`

  `docker-compose exec web python manage.py migrate --noinput`

Сбор статических файлов:

  `docker-compose exec web python manage.py collectstatic --no-input`
  
Проект запущен и доступен по адресу [http://localhost/](http://localhost/).

Создаем суперпользователя:

  `docker-compose exec web python manage.py createsuperuser`

Заполнения базы начальными данными:

  `docker-compose exec web python manage.py loaddata fixtures.json`

Остановить все запущенные контейнеры:

  `docker-compose down`

## Автор:
[Аксентий Виктория](https://github.com/wiky-avis)
