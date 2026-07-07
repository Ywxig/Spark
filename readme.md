#  Spark

**Spark** — a web-based manager for your code solutions. Organize projects, manage files, and open them in your IDE directly from the browser.

---

## Installation

### 0. Needed things
- Python 3.14+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/your-user/spark.git
cd spark
```

### 2. Add an alias (recommended)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias spark="python /path/to/spark/run.py"
```

Then apply:

```bash
source ~/.bashrc
```

> After this, all commands can be called as `spark <command>` instead of `python run.py <command>`.

---

## Running

```bash
spark run
```

On first launch, Spark will automatically create a `.venv` virtual environment and install all dependencies from `requirements.txt`.

The app will open in the browser automatically (if enabled in `config.json`).

To stop — press `Ctrl+C`.

---

## Commands

| Command | Description |
|---|---|
| `spark run` | Start the web application |
| `spark update` | Update Spark from GitHub (branch `master`) |
| `spark version` | Show current version |
| `spark setup` |  |
| `spark explorer [LOCATION]`|  |

### `spark update`

```bash
spark update                    # update from master branch
spark update --branch dev       # update from a specific branch
```

>  `update` performs a `git reset --hard` — any local changes inside the Spark folder will be discarded. If you want to keep them, commit before updating.

---

## Interface

After starting, open your browser at the address configured in `config.json` (default `http://localhost:5000`).

| Page | URL | Description |
|---|---|---|
| Home | `/` | List of all solutions |
| Create | `/create` | New solution (from template or blank) |
| Solution | `/solution/<name>` | Detail page with files and readme |
| Documentation | `/docs` | Built-in documentation |
| Settings | `/option` | Application settings |
| Profile | `/user` | User statistics |
| Migrations | `/migrate` | Import solutions from another directory |

---

## Configuration (`config.json`)

```jsonc
{
  "VERSION": "1.0.0",
  "DEBUG_MODE": true,

  "START_OPTIONS": {
    "host": "0.0.0.0",
    "ip": "127.0.0.1",
    "port": 8000,
    "open_in_browser": true,
    "check_open_in_browser": true   // don't reopen on hot-reload
  },

  "IDE": {
    "open_in_ide": true,
    "path": "",                     // path to IDE executable (if not in PATH)
    "cmd": {
      "open": "code"                // open command (code, idea, subl, ...)
    }
  },

  "MIGRATION_DIR": "/path/to/old/solutions",
  "SRC_DIR": "src",

  "WATCHDOG_ENABLED": true,
  "WATCHDOG_TIMEOUT": 60            // seconds before auto-shutdown when all tabs are closed
}
```

### Watchdog

If `WATCHDOG_ENABLED: true` — Spark will automatically shut down after `WATCHDOG_TIMEOUT` seconds once all browser tabs are closed. Useful to avoid leaving the server running idle.

---

## API

Basic REST API for integrations:

```
GET  /api/solutions          — list all solutions
GET  /api/solutions/<name>   — get a specific solution
POST /api/ping               — heartbeat (used by the watchdog)
POST /api/user-session-end   — end session and stop the server
```

---

## Project Structure

```
spark/
├── main.py              # Flask application
├── run.py               # CLI launch utility
├── config.json          # Configuration
├── requirements.txt     # Dependencies
├── src/
│   ├── Solution_Manager/ # Solution management logic
│   └── loger/           # Logger
└── templates/           # Jinja2 templates
```

---

## Requirements

- Python 3.10+
- Git (for `spark update`)
- A modern browser


#  Spark

**Spark** — веб-менеджер для твоих code-решений. Организуй проекты, управляй файлами и открывай их в IDE прямо из браузера.

---

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-user/spark.git
cd spark
```

### 2. Добавить алиас (рекомендуется)

Добавь в `~/.bashrc` или `~/.zshrc`:

```bash
alias spark="python /path/to/spark/run.py"
```

Затем примени:

```bash
source ~/.bashrc
```

> После этого все команды можно вызывать как `spark <команда>` вместо `python run.py <команда>`.

---

## Запуск

```bash
spark run
```

Spark сам создаст виртуальное окружение `.venv` и установит все зависимости из `requirements.txt` при первом запуске.

После старта приложение откроется в браузере автоматически (если включено в `config.json`).

Для остановки — `Ctrl+C`.

---

## Команды

| Команда | Описание |
|---|---|
| `spark run` | Запустить веб-приложение |
| `spark update` | Обновить Spark с GitHub (ветка `master`) |
| `spark version` | Показать текущую версию |

### `spark update`

```bash
spark update                    # обновление с ветки master
spark update --branch dev       # обновление с другой ветки
```

>  `update` делает `git reset --hard` — локальные изменения в папке Spark будут сброшены. Если хочешь их сохранить — закоммить перед обновлением.

---

## Интерфейс

После запуска открой браузер по адресу из `config.json` (по умолчанию `http://localhost:5000`).

| Страница | URL | Описание |
|---|---|---|
| Главная | `/` | Список всех решений |
| Создать | `/create` | Новое решение (с шаблоном или без) |
| Решение | `/solution/<name>` | Детальная страница, файлы, readme |
| Документация | `/docs` | Встроенная документация |
| Настройки | `/option` | Параметры приложения |
| Профиль | `/user` | Статистика пользователя |
| Миграции | `/migrate` | Импорт решений из другой папки |

---

## Конфигурация (`config.json`)

```jsonc
{
  "VERSION": "1.0.0",
  "DEBUG_MODE": true,

  "START_OPTIONS": {
    "host": "0.0.0.0",
    "ip": "127.0.0.1",
    "port": 5000,
    "open_in_browser": true,
    "check_open_in_browser": true   // не открывать повторно при hot-reload
  },

  "IDE": {
    "open_in_ide": true,
    "path": "",                     // путь к исполняемому файлу IDE (если не в PATH)
    "cmd": {
      "open": "code"                // команда открытия (code, idea, subl, ...)
    }
  },

  "MIGRATION_DIR": "/path/to/old/solutions",
  "SRC_DIR": "src",

  "WATCHDOG_ENABLED": true,
  "WATCHDOG_TIMEOUT": 60            // секунд до автоостановки, если все вкладки закрыты
}
```

### Watchdog

Если `WATCHDOG_ENABLED: true` — Spark автоматически завершится через `WATCHDOG_TIMEOUT` секунд после того, как все вкладки браузера будут закрыты. Удобно, чтобы не держать сервер запущенным вхолостую.

---

## API

Базовый REST API для интеграций:

```
GET  /api/solutions          — список всех решений
GET  /api/solutions/<name>   — данные конкретного решения
POST /api/ping               — heartbeat (используется watchdog'ом)
POST /api/user-session-end   — завершить сессию и остановить сервер
```

---

## Структура проекта

```
spark/
├── main.py              # Flask-приложение
├── run.py               # CLI-утилита запуска
├── config.json          # Конфигурация
├── requirements.txt     # Зависимости
├── src/
│   ├── Solution_Manager/ # Логика управления решениями
│   └── loger/           # Логгер
└── templates/           # Jinja2-шаблоны
```

---

## Требования

- Python 3.10+
- Git (для `spark update`)
- Браузер