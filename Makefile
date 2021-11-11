run:
	docker-compose up -d --build

stop:
	docker-compose stop

rm:
	docker-compose rm --stop -v --force
