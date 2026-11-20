# Студия танцев — CI/CD + Docker

Flask-приложение для управления танцевальной студией. ЛР1: CRUD API, pytest, Jenkins Pipeline. ЛР2: контейнеризация (Docker), веб-сервер nginx, микросервисная архитектура.

## Сущности
- `classes` — занятия (`title`, `instructor_id`, `style_id`, `studio_id`, `duration` в минутах)
- `instructors` — преподаватели (`name`)
- `styles` — стили танцев (`name`)
- `studios` — залы (`name`)

Для каждой сущности доступны POST, GET списка, GET по ID, PUT, DELETE. Всего 20 CRUD-операций.

## Архитектура (ЛР2)
```
Браузер ──:80──> [ nginx ] ──сеть backend──> [ app: gunicorn + Flask :5000 ] ──> том dance-data (SQLite)
```
- `app` — образ из `Dockerfile` (Python 3.12, gunicorn), порт 5000 наружу не открыт
- `nginx` — образ из `nginx/Dockerfile`, reverse proxy, порт 80
- `docker-compose.yml` — описывает оба сервиса, сеть `backend` и том `dance-data`

## Запуск в Docker
```powershell
docker compose up -d --build
docker compose ps
curl.exe http://localhost/health
```
Сайт: http://localhost  
Остановка: `docker compose down` (данные в томе сохраняются; `docker compose down -v` удалит и их).

## Запуск без Docker (как в ЛР1)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe run.py
```

## Jenkins
Multibranch Pipeline. На всех ветках: сборка образов, pytest внутри контейнера, проверка конфига nginx (`nginx -t`). Только на `main`: развёртывание через `docker compose up -d` и Health Check `http://localhost/health`.  
Служба Jenkins должна иметь доступ к Docker Desktop (запуск службы от учётной записи пользователя, состоящего в группе `docker-users`).

Не добавляйте `.venv`, `.git` и локальные файлы БД в Git-репозиторий.
