up:
	docker-compose up -d

build:
	docker-compose up -d --force-recreate --build

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

dumpdata:
	docker-compose exec backend python manage.py dumpdata > fixtures.json

loaddata:
	docker-compose exec backend python manage.py loaddata fixtures.json
