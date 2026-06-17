# Service P

Асинхронный REST API сервис для работы с пользователями, счетами и платежами.

Стек: **FastAPI · SQLAlchemy 2 (async) · PostgreSQL · Alembic · dependency-injector ·
JWT · Docker Compose**.


---

## Возможности

**Пользователь:**
- авторизация по email/password (JWT);
- получение данных о себе (`id`, `email`, `full_name`);
- список своих счетов с балансами;
- список своих платежей.

**Администратор:**
- авторизация по email/password (JWT);
- получение данных о себе;
- создание / обновление / удаление пользователей;
- список пользователей со списком их счетов и балансов.

**Платежи:**
- роут-вебхук, эмулирующий обработку события от сторонней платёжной системы:
  проверка подписи → создание счёта, если его нет → сохранение транзакции →
  начисление суммы на баланс. Транзакции идемпотентны (один `transaction_id`
  начисляется ровно один раз).

---

## Архитектура

clean architecture, DDD, DI.

## Запуск через Docker Compose

```bash
docker compose up -d --build      # или: make run
```

- API:     http://localhost:8000
- Swagger: http://localhost:8000/docs

Остановка:

```bash
docker compose down        # make stop
docker compose down -v     # вместе с данными БД
```

---

## Запуск без Docker

Нужны Python 3.12+ и доступный PostgreSQL.

```bash
# 1) (опционально) поднять только Postgres
docker run -d --name service-p-db \
  -e POSTGRES_DB=service_p -e POSTGRES_USER=app -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 postgres:16-alpine

# 2) установить зависимости
cd app
poetry install            # если нет poetry: pip install poetry

# 3) указать строку подключения (переменные окружения важнее значений из envs/app.env)
export APP__DB__URL="postgresql+asyncpg://app:secret@localhost:5432/service_p"
export APP__WEBHOOK_SECRET_KEY="gfdmhghif38yrf9ew0jkf32"
export APP__JWT__SECRET="dev-secret"

# 4) применить миграции (создаёт схему + тестовые данные)
poetry run alembic upgrade head

# 5) запустить приложение
cd src
poetry run uvicorn main:main_app --host 0.0.0.0 --port 8000
# либо в проде:
# poetry run gunicorn main:main_app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## Переменные окружения

Префикс `APP__`, вложенность через `__`. Значения по умолчанию — в `envs/app.env`.

| Переменная                          | Описание                              | По умолчанию |
|-------------------------------------|---------------------------------------|--------------|
| `APP__DB__URL`                      | URL PostgreSQL (asyncpg)              | —            |
| `APP__JWT__SECRET`                  | Секрет для подписи JWT                | `change-me`  |
| `APP__JWT__ALGORITHM`               | Алгоритм JWT                          | `HS256`      |
| `APP__JWT__ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена (мин)          | `60`         |
| `APP__WEBHOOK_SECRET_KEY`           | Секрет для подписи вебхуков           | `gfdmhghif38yrf9ew0jkf32` |
| `APP__LOG_LEVEL`                    | Уровень логирования                   | `INFO`       |
| `APP__VERSION`                      | `dev` / `prod` (формат логов)         | `dev`        |

---

