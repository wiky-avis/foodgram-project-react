up:
	docker-compose up -d

build:
	docker-compose up -d --build

isort:
	isort .

makemigrations:
	docker-compose exec backend python manage.py makemigrations

migrate:
	docker-compose exec backend python manage.py migrate --noinput

static:
	docker-compose exec backend python manage.py collectstatic --no-input

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

down:
	docker-compose down

loaddata_fixtures:
	docker-compose exec backend python manage.py load_data
