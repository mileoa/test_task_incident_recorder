DC = docker compose 
LOGS = docker logs 
ENV = --env-file ./src/.env
EXEC = docker exec -it
MANAGE_PY = python manage.py

STORAGES_FILE = docker/storages.yaml
DB_CONTAINER = cash-flow-db

APP_FILE = docker/app.yaml
APP_CONTAINER = incident-recorder-main-app

NGINX_FILE = docker/nginx.yaml
NGINX_CONTAINER = nginx


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${NGINX_FILE} ${ENV} up -d

.PHONY: app-rebuild
app-rebuild:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${NGINX_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} down 

.PHONY: db-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: test
test:
	PYTHONPATH=src pytest --ds=core.settings.test tests
