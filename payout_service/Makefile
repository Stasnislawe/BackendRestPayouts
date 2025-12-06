.PHONY: help install migrate run test worker docker-up docker-down lint format
.PHONY: migrate-docker run-docker worker-docker test-docker shell-docker logs

help:
	@echo "Доступные команды:"
	@echo ""
	@echo "Локальная разработка (с Poetry):"
	@echo "  install     - установка зависимостей через Poetry"
	@echo "  migrate     - применение миграций (локально)"
	@echo "  run         - запуск Django сервера (локально)"
	@echo "  worker      - запуск Celery worker (локально)"
	@echo "  test-api        - запуск тестов (локально)"
	@echo "  test-tasks        - запуск тестов (локально)"
	@echo "  lint        - проверка кода линтерами"
	@echo "  format      - форматирование кода"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up        - запуск всех сервисов через Docker"
	@echo "  docker-down      - остановка Docker сервисов"
	@echo "  migrate-docker   - применение миграций в Docker контейнере"
	@echo "  run-docker       - запуск только веб-сервера в Docker"
	@echo "  worker-docker    - запуск только Celery worker в Docker"
	@echo "  test-api-docker      - запуск тестов в Docker контейнере"
	@echo "  test-tasks-docker      - запуск тестов в Docker контейнере"
	@echo "  shell-docker     - войти в shell веб-контейнера"
	@echo "  logs             - просмотр логов всех контейнеров"
	@echo ""
	@echo "Для разработки используйте: make docker-up"
	@echo "Для локального тестирования: make install && make run"

# ========== Локальная разработка (Poetry) ==========
install:
	poetry install

migrate:
	poetry run python manage.py migrate

run:
	poetry run python manage.py runserver

worker:
	celery -A config worker --pool=solo --loglevel=info

test-api:
	python manage.py test payouts.tests.test_api

test-tasks:
	python manage.py test payouts.tests.test_tasks

lint:
	poetry run black --check src/
	poetry run flake8 src/
	poetry run mypy src/

format:
	poetry run black src/

# ========== Docker разработка ==========
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down -v

migrate-docker:
	docker-compose exec web python manage.py migrate

run-docker:
	docker-compose up web

worker-docker:
	docker-compose up celery

test-api-docker:
	docker-compose exec web python manage.py test payouts.tests.test_api

test-tasks-docker:
	docker-compose exec web python manage.py test payouts.tests.test_tasks

shell-docker:
	docker-compose exec web sh

logs:
	docker-compose logs -f

# ========== Производственные команды ==========
setup-dev: install migrate
	@echo "Локальное окружение разработки настроено!"

clean:
	docker-compose down -v
	rm -rf src/__pycache__ src/payouts/__pycache__ src/payouts/migrations/__pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# ========== Комбинации команд ==========
full-reset: clean docker-down docker-up migrate-docker
	@echo "Полный сброс и перезапуск выполнен!"