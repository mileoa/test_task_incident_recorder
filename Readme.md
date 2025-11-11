# Учет инцедентов

## Требования к окружению

- Git
- Docker
- Linux

## Установка и запуск

1. Клонирование репозитория:
```bash
git clone git@github.com:mileoa/test_task_incident_recorder.git
cd test_task_incident_recorder
```

2. Создайте файл `src/.env`. Команда для создания файла из корня проекта:
```bash
echo 'POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_postgres_password"
POSTGRES_INTERNAL_PORT="5432"
POSTGRES_HOST="cash-flow-db"
POSTGRES_DB="cash_flow"

DJANGO_SECRET_KEY="your_django_secret_key"
DJANGO_HOST="http://localhost:8081"' > src/.env
```
DJANGO_HOST - адрес по которому доступно приложение.

3. Если нужно изменить порт (по умолчанию 8081):
- Откройте файл `docker/nginx.yaml`
- Замените `8081` на желаемый порт в секции `ports`
- В src/.env в параметре DJANGO_HOST установите новый порт

4. Выполнить запуск приложения, миграции и создание суперпользователя по очерди. Выполнять в корне проекта, где лежит файл Makefile:
```bash
make app
make migrate
```

4.1 При необходимости создайте суперпользователя
```bash
make superuser
```

5. Приложение по умолчанию будет доступно по адресу:
   http://localhost:8081

6. Примеры запросов можете увидите через swagger по адресу http://localhost:8081/swagger/
7. Примеры запросов:
```bash
# Получение списка инцидентов со статусом "new"
curl -X 'GET' 'http://localhost:8081/api/incidents/?status=new' -H 'accept: application/json'

# Создание нового инцидента
curl -X 'POST' \
  'http://localhost:8081/api/incidents/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "string",
  "status": "new",
  "source": "operator"
}'

# Обновление инцидента по id
curl -X 'PATCH' \
  'http://localhost:8081/api/incidents/1/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "string",
  "status": "new",
  "source": "operator"
}'

# Обновление инцидента по id
curl -X 'PUT' \
  'http://localhost:8081/api/incidents/1/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "string",
  "status": "new",
  "source": "operator"
}'
```