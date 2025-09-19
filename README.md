### Drum Practice Tracker

## Для чего нужен проект
Приложение для отслеживания тренировок по ударным. Основные возможности:
- **Пользователь** (`users.User`) создаёт **сессии тренировок** (`training.TrainingSession`).
- При создании пользователя автоматически создаётся **статистика** `users.Stats` (OneToOne с пользователем).
- При создании тренировки срабатывает сигнал, который публикует событие в **RabbitMQ**; фоновый воркер читает очередь и пересчитывает агрегированную статистику (кол-во сессий, суммарные минуты, средняя длительность, дата последнего пересчёта).

Технологии: Django 5, PostgreSQL, RabbitMQ (aio-pika), Docker Compose, Poetry.

## Инструкция по развертыванию

### Подготовка .env
В корне создайте файл `.env` со значениями (пример):
```
# PostgreSQL (в docker-compose нет сервиса БД — используйте внешний Postgres)
DB_NAME=drum_db
DB_USER=drum_user
DB_PASSWORD=drum_password
DB_HOST=localhost
DB_PORT=5432

# RabbitMQ
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBIT_MQ_CONTAINER=drums_rabbitmq
RABBIT_MQ_PORT=5672
```

Примечание: в `settings.py` настроен `AUTH_USER_MODEL = 'users.User'` и используется PostgreSQL через переменные окружения. Нужен доступный внешний Postgres (или адаптируйте конфиг под SQLite на время разработки).

### Запуск через Docker Compose (рекомендуется)
1) Соберите и поднимите сервисы:
```
docker compose up --build
```
Будут запущены:
- Django-приложение на 8000 порту (`http://localhost:8000`)
- RabbitMQ (AMQP: 5672, UI: `http://localhost:15672`)
- Фоновый воркер, слушающий очередь `training_events`

2) Примените миграции и создайте суперпользователя:
```
docker exec -it drum-practice-tracker poetry run python manage.py migrate
docker exec -it drum-practice-tracker poetry run python manage.py createsuperuser
```

3) Проверьте работу:
- Создайте пользователя — объект `users.Stats` создастся автоматически.
- Создайте `training.TrainingSession` — в логах Django увидите срабатывание сигналов, в логах воркера — пересчёт статистики.

Остановить сервисы:
```
docker compose down
```

### Локальный запуск без Docker
Требуется установленный Python 3.10+, Poetry, внешний PostgreSQL и RabbitMQ.

1) Установите зависимости:
```
poetry install
```

2) Убедитесь, что `.env` заполнён корректно (см. выше).

3) Примените миграции и создайте суперпользователя:
```
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

4) Запустите сервер и воркер (в разных терминалах):
```
poetry run python manage.py runserver 0.0.0.0:8000
poetry run python rabbit_mq_worker.py
```

### Ключевые файлы
- `users/models.py` — `User`, `Stats`
- `users/signals.py` — создание `Stats` при создании пользователя (регистрируется через `users.apps.UsersConfig.ready`)
- `training/models.py` — `TrainingSession`
- `training/signals.py` — публикация события в RabbitMQ при создании сессии (регистрируется через `training.apps.TrainingConfig.ready`)
- `rabbit_mq_worker.py` — потребитель очереди `training_events`, пересчёт `Stats`
- `docker-compose.yaml` — Django, RabbitMQ, воркер


