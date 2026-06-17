DC   = docker compose
EXEC = docker exec -it

APP_CONTAINER = service-p-api


.PHONY: run
run: stop
	$(DC) up -d --build

.PHONY: stop
stop:
	$(DC) down

.PHONY: build
build:
	$(DC) build

.PHONY: logs
logs:
	$(DC) logs -f -n 1000

.PHONY: migrate
migrate:
	$(EXEC) $(APP_CONTAINER) poetry run alembic upgrade head

.PHONY: shell
shell:
	$(EXEC) $(APP_CONTAINER) bash
