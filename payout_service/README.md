# Быстрый старт через Docker 
## Нужно запустить Docker

# 1. Клонируйте репозиторий
```bash
git clone <ваш-репозиторий>
cd BackendPayoutsREST
```

# 2. Перейдите в директорию проекта
```bash
cd payout_service
```

# 3. Запустите все сервисы
## В файле .env замените параметры на свои, после запускайте сервисы
```bash
make docker-up
```

# 4. Примените миграции (в новом терминале)
```bash
make migrate-docker
```

# 5. Откройте в браузере:
###    - API: http://localhost:8000/api/v1/payouts/
###    - Swagger: http://localhost:8000/api/docs/
###    - Admin: http://localhost:8000/admin/

# Старт без Docker`а
# 1. Установите зависимости

```bash
make install
```

# 2. Установите и запустите PostgreSQL 16 и Redis
## Также можно запустить Redis через Docker:
``bash
celery -A config worker --pool=solo --loglevel=info
``

# 3. Настройте .env файл

```bash
# Отредактируйте .env файл
```

### _!!! Обязательно в настройках  (config/settings.py) в настройках базы данных (89 строчка замените postgres на localhost)_

# 4. Примените миграции

```bash
make migrate
```
# 5. Запустите сервер

```bash
make run
```
# 6. В другом терминале запустите Celery worker

```bash
make worker
```

# 7. Откройте в браузере:
###    - API: http://localhost:8000/api/v1/payouts/
###    - Swagger: http://localhost:8000/api/docs/
###    - Admin: http://localhost:8000/admin/