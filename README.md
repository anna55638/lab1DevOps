# Студия танцев — CI/CD

Адаптация исходного Flask-проекта библиотеки под управление танцевальной студией. Сохранены структура, интерфейс, CRUD API, pytest и Jenkins Pipeline.

## Сущности
- `classes` — занятия (`title`, `instructor_id`, `style_id`, `studio_id`, `duration` в минутах)
- `instructors` — преподаватели (`name`)
- `styles` — стили танцев (`name`)
- `studios` — залы (`name`)

Для каждой сущности доступны POST, GET списка, GET по ID, PUT, DELETE. Всего 20 CRUD-операций.

## Запуск в Windows (PowerShell)
1. Установите Python с включённым **Add python.exe to PATH**.
2. Откройте PowerShell в папке проекта и выполните:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe run.py
```

Сайт: http://127.0.0.1:5000

## Jenkins на Windows
Jenkinsfile оставлен как в исходнике, **кроме** строки `PYTHON = 'python'`. Python должен находиться в PATH **учётной записи службы Jenkins**. Проверьте это в Jenkins Pipeline командой `bat 'where python'` или в системе. Если служба не видит Python, добавьте путь к папке Python в системную PATH и перезапустите службу Jenkins.

**Важно:** в соответствии с просьбой сохранить Jenkinsfile, исходные имена `LibraryApp` и путь `C:\deploy\library` в этапах развёртывания НЕ изменены. Это только внутренние имена задачи и каталога; приложение при этом танцевальное. Jenkins разворачивает приложение только из ветки `main`, используя Windows Task Scheduler, и требует права на регистрацию задач. На Windows Jenkins Agent должны быть доступны `python`, `powershell`, `robocopy`, `curl.exe`.

Не добавляйте `.venv`, `.git` и локальные файлы БД в Git-репозиторий.
