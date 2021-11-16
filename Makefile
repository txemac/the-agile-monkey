help:
	@echo 'Makefile for managing API                                  '
	@echo '                                                           '
	@echo 'Usage:                                                     '
	@echo ' make build        build images                            '
	@echo ' make up           creates containers and starts service   '
	@echo ' make migrate-up   run all migration                       '
	@echo ' make pytest       run tests                               '
	@echo ' make down         stops service and removes containers    '
	@echo ' make stop         stops service containers                '
	@echo ' make rm           stop and remove containers and volumes  '
	@echo '                                                           '

build:
	docker-compose build

up:
	docker-compose up -d

migrate-up:
	docker-compose exec api alembic upgrade head

pytest:
	docker-compose exec -e DATABASE_URL=postgresql://postgres:postgres@db/database_test api pytest -vvv

down:
	docker-compose down

stop:
	docker-compose stop

rm:
	docker-compose rm --stop -v --force
