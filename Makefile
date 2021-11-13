help:
	@echo 'Makefile for managing web application                              '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make build            build images                                '
	@echo ' make up               creates containers and starts service       '
	@echo ' make migrate-up       run all migration                           '
	@echo ' make down             stops service and removes containers        '
	@echo ' make stop             stops service containers                    '
	@echo ' make rm               stop and remove containers and volumes      '
	@echo '                                                                   '

build:
	docker-compose build

up:
	docker-compose up -d

migrate-up:
	docker-compose exec api alembic upgrade head

down:
	docker-compose down

stop:
	docker-compose stop

rm:
	docker-compose rm --stop -v --force
