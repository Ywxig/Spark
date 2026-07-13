"""
Flask приложение для управления решениями.
Запуск: python app.py
"""

import subprocess
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.Solution_Manager import SolutionManager, Solution, Migrations
from config_loader import ConfigLoader
from src.Solution_Manager.template import Template

from src.loger import Logger
from src.git_client import GitClient
import markdown

import signal
import time
import threading

import os
import sys

app = Flask(__name__)
manager = SolutionManager()
cfg = ConfigLoader("config.json").load()



@app.context_processor
def inject_config():
    """
    Inject configuration into all template contexts.
    
    This function is registered as a Flask context processor to make the
    application configuration available in all Jinja2 templates without
    explicitly passing it in each route.
    
    Returns:
        dict: A dictionary containing the configuration object accessible
              as 'config' variable in templates.
    """
    return dict(config=cfg)


def _to_bool(value):
    """Приводит значение чекбокса из формы к bool."""
    return str(value).strip().lower() in ("true", "1", "on", "yes")


def _to_int(value, default):
    """Безопасно приводит строку из формы к int, при ошибке — default."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def build_config_from_form(form, current_cfg):
    """
    Собирает новый словарь конфигурации на основе данных формы страницы настроек.

    Чекбоксы, которые не были отмечены, отсутствуют в form — для них
    подставляется False. Поля, не представленные на странице настроек
    (например MIGRATION), переносятся из текущего конфига без изменений.

    Args:
        form: request.form (ImmutableMultiDict) со страницы /option.
        current_cfg: текущий загруженный конфиг (для значений по умолчанию).

    Returns:
        dict: новый конфиг, готовый для сохранения в config.json.
    """
    def get(key, default=""):
        return form.get(key, default).strip()

    log_cfg = current_cfg.get("LOG", {}) or {}
    author_cfg = current_cfg.get("AUTHOR", {}) or {}
    start_cfg = current_cfg.get("START_OPTIONS", {}) or {}
    ide_cfg = current_cfg.get("IDE", {}) or {}
    ide_cmd_cfg = ide_cfg.get("cmd", {}) or {}

    links_raw = get("AUTHOR.LINKS", ", ".join(author_cfg.get("LINKS", []) or []))
    links = [link.strip() for link in links_raw.split(",") if link.strip()]

    new_cfg = {
        "SOLUTION_DIR": get("SOLUTION_DIR", current_cfg.get("SOLUTION_DIR", "")),
        "APP_NAME": get("APP_NAME", current_cfg.get("APP_NAME", "")),
        "SRC_DIR": get("SRC_DIR", current_cfg.get("SRC_DIR", "")),
        "CONFIG_FILE": get("CONFIG_FILE", current_cfg.get("CONFIG_FILE", "config.json")),
        "MIGRATION_DIR": get("MIGRATION_DIR", current_cfg.get("MIGRATION_DIR", "")),
        "CODE_TEMPLATE_DIR": get("CODE_TEMPLATE_DIR", current_cfg.get("CODE_TEMPLATE_DIR", "")),
        "DEBUG_MODE": _to_bool(form.get("DEBUG_MODE")),

        "LOG": {
            "LEVEL": get("LOG.LEVEL", log_cfg.get("LEVEL", "INFO")),
            "FILE": get("LOG.FILE", log_cfg.get("FILE", "app.log")),
        },

        "AUTHOR": {
            "NAME": get("AUTHOR.NAME", author_cfg.get("NAME", "")),
            "AVATAR": get("AUTHOR.AVATAR", author_cfg.get("AVATAR", "")),
            "GITHUB": get("AUTHOR.GITHUB", author_cfg.get("GITHUB", "")),
            "LANGUAGE": get("AUTHOR.LANGUAGE", author_cfg.get("LANGUAGE", "en")),
            "EMAIL": get("AUTHOR.EMAIL", author_cfg.get("EMAIL", "")),
            "LINKS": links,
        },

        "START_OPTIONS": {
            "open_in_browser": _to_bool(form.get("START_OPTIONS.open_in_browser")),
            "check_open_in_browser": _to_bool(form.get("START_OPTIONS.check_open_in_browser")),
            "port": _to_int(get("START_OPTIONS.port", str(start_cfg.get("port", 5000))), start_cfg.get("port", 5000)),
            "host": get("START_OPTIONS.host", start_cfg.get("host", "127.0.0.1")),
        },

        "IDE": {
            "open_in_ide": _to_bool(form.get("IDE.open_in_ide")),
            "open_in_ide_cmd": _to_bool(form.get("IDE.open_in_ide_cmd")),
            "name": get("IDE.name", ide_cfg.get("name", "")),
            "path": get("IDE.path", ide_cfg.get("path", "")),
            "cmd": {
                "open": get("IDE.cmd.open", ide_cmd_cfg.get("open", "code")),
            },
        },

        "WATCHDOG_ENABLED": _to_bool(form.get("WATCHDOG_ENABLED", current_cfg.get("WATCHDOG_ENABLED"))),
        "WATCHDOG_TIMEOUT": _to_int(
            get("WATCHDOG_TIMEOUT", str(current_cfg.get("WATCHDOG_TIMEOUT", 60))),
            current_cfg.get("WATCHDOG_TIMEOUT", 60),
        ),
        "VERSION" : current_cfg.get("VERSION", "unknown"),
    }

    # Раздел MIGRATION не редактируется на странице настроек — сохраняем как есть
    if "MIGRATION" in current_cfg:
        new_cfg["MIGRATION"] = current_cfg["MIGRATION"]

    return new_cfg


def save_config(data, path):
    """Сохраняет словарь конфигурации в JSON-файл (с отступами, UTF-8)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Страницы

@app.route("/")
def index():
    """Список всех решений."""
    solutions = manager.index()
    return render_template("index.html", solutions=solutions)

@app.route("/migrate", methods=["GET", "POST"])
def migrate():
    """Панель с настройкой миграции"""
    migrations = Migrations().index()    
    return render_template("migration.html", migrations=migrations)

@app.route("/migrate/run", methods=["GET", "POST"])
def migrate_run():
    migrate_msg = Migrations.migrate(source_dir=cfg["MIGRATION_DIR"])
    Logger().info(f"[MIGRATE] Done. {migrate_msg}")
    return redirect(url_for("index"))   

@app.route("/docs")
def documentation():
    """Place for documentation. About all what user need to know."""
    return render_template("docs/main.html")

@app.route("/solution/<name>")
def solution_detail(name):
    """Детальная страница решения."""
    try:
        solution = manager.get(name)
        files = solution.list_sources()
        return render_template("detail.html", solution=solution, files=files, readme_md=markdown.markdown(solution.read_source("readme.md"), extensions=["extra"]))
    except FileNotFoundError or Exception as e:
        print(f"[ERROR](solution_detail) {name}: {e}")
        return render_template("errors/404.html", error=e), 404

@app.route("/option", methods=["GET", "POST"])
def option():
    """Панель настроек"""
    global cfg
    error = None
    success = None

    if request.method == "POST":
        try:
            new_cfg = build_config_from_form(request.form, cfg)
            save_config(new_cfg, cfg.get("CONFIG_FILE", "config.json"))
            cfg = ConfigLoader(cfg.get("CONFIG_FILE", "config.json")).load()
            success = "Настройки успешно сохранены."
        except Exception as e:
            error = f"Не удалось сохранить настройки: {e}"

    return render_template("option.html", config=cfg, error=error, success=success)

@app.route("/create", methods=["GET", "POST"])
def create():
    """Создать новое решение."""
    templates = Template.index()  # <- добавить

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        template = request.form.get("template", "").strip() or None
        readme_text = request.form.get("readme", "").strip() or None
        origin = request.form.get("origin", "")

        if not name:
            return render_template("create.html", error="Имя не может быть пустым.", templates=templates)

        try:
            if template is not None:
                Template(template).create(name, description, readme_text, origin)
            else:
                manager.create(Name=name, Description=description)
            return redirect(url_for("solution_detail", name=name))
        except FileExistsError:
            return render_template("create.html", error=f"Решение «{name}» уже существует.", templates=templates)

    return render_template("create.html", templates=templates)  # <- передать

@app.route("/solution/<name>/git", methods=["GET"])
def git_control(name):
    """Git repository management for a solution."""
    # Validate solution name: only letters, digits, hyphens and underscores allowed
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return render_template("git_control.html", error="Invalid solution name."), 400
    
    # Check if solution exists
    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return render_template("git_control.html", error=f"Solution '{name}' not found."), 404
    
    return render_template("git_control.html", solution=solution)

@app.route("/solution/<name>/delete", methods=["POST"])
def delete(name):
    """Удалить решение."""
    try:
        manager.delete(name)
    except FileNotFoundError:
        pass

    return redirect(url_for("index"))


@app.route("/solution/<name>/open", methods=["POST"])
def open_in_ide(name):
    """Открыть папку решения в редакторе из конфига (IDE.cmd.open).

    Args:
        name (str): Имя решения, которое необходимо открыть.

    Returns:
        Response: JSON-ответ с результатом операции.
            - 200 OK: {"ok": True, "opened": "<путь_к_решению>"}
            - 400 Bad Request: Если функция открытия отключена или команда не задана.
            - 404 Not Found: Если решение с указанным именем не найдено.
            - 500 Internal Server Error: Если исполняемый файл редактора не найден.
    """
    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return jsonify({"error": "Решение не найдено"}), 404

    ide = cfg.get("IDE", {})

    # Проверка включения функции открытия в IDE и наличия команды
    if not ide.get("open_in_ide"):
        return jsonify({"error": "open_in_ide отключён в config.json"}), 400

    cmd = ide.get("cmd", {}).get("open", "").strip() # Получение команды открытия в IDE
    if not cmd:
        return jsonify({"error": "IDE.cmd.open не задан в config.json"}), 400

    # Если задан явный путь к исполняемому файлу — используем его,
    # иначе берём команду из PATH (например, "code")
    exe_path = ide.get("path", "").strip()
    executable = exe_path if exe_path else cmd

    try:
        subprocess.Popen([executable, str(solution.path) + "/" + cfg["SRC_DIR"]])
        return jsonify({"ok": True, "opened": str(solution.path)})
    except FileNotFoundError:
        return jsonify({"error": f"Редактор «{executable}» не найден. Проверь IDE.path в config.json"}), 500
    

@app.route("/solution/<name>/explorer", methods=["POST"])
def open_in_explorer(name):
    """Открыть папку решения в проводнике.
    если ос = линукс то используем xdg-open
    но если ос = windows то используем explorer.exe

    Args:
        name (str): Имя решения, которое необходимо открыть.

    Returns:
        Response: JSON-ответ с результатом операции.
            - 200 OK: {"ok": True, "opened": "<путь_к_решению>"}
            - 400 Bad Request: Если функция открытия отключена или команда не задана.
            - 404 Not Found: Если решение с указанным именем не найдено.
            - 500 Internal Server Error: Если исполняемый файл редактора не найден.
    """

    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return jsonify({"error": "Solution not find"}), 404

    try:
        if sys.platform == "linux":
            subprocess.Popen(["xdg-open", str(solution.path)])
        elif sys.platform == "win32":
            subprocess.Popen(["explorer", str(solution.path)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(solution.path)])
        else:
            return jsonify({"error": f"unknown platform: {sys.platform}"}), 400
        
        return jsonify({"ok": True, "opened": str(solution.path)}), 200
    except Exception as e:
        return jsonify({"error": f"Error! can not open folder: {str(e)}"}), 500

# API (JSON)
@app.route("/api/solutions")
def api_solutions():
    solutions = manager.index()
    return jsonify([{
        "name": s.Name,
        "description": s.Description,
        "files": s.list_sources(),
    } for s in solutions])

@app.route("/api/user-session-end", methods=["POST"])
def user_session_end():
    """
    Handle user session end.
    
    This endpoint is used to handle the user session end event.
    It can be used to perform any necessary cleanup tasks or actions
    when a user session ends.
    
    Returns:
        tuple: A tuple containing the rendered "user_session_end.html" template
               and the HTTP status code 200.
    """
    os.kill(os.getpid(), signal.SIGINT)

# Saving time of last ping
LAST_HEARTBEAT = time.time()

def watchdog():
    '''Background thread, which watchdogs user activity'''
    global LAST_HEARTBEAT
    while True:
        time.sleep(1)
        # If pings are less than `cfg["WATCHDOG_TIMEOUT"]` seconds — continue
        if time.time() - LAST_HEARTBEAT > cfg["WATCHDOG_TIMEOUT"]:
            print("ALL TABS ARE CLOUSED, KILL PROCESS...")
            os.kill(os.getpid(), signal.SIGINT)
            break


@app.route("/api/git/status/<name>", methods=["GET"])
def git_status(name):
    """
    Возвращает статус git-репозитория для конкретного решения.
 
    Args:
        name (str): Имя решения.
 
    Returns:
        200: {"branch": str, "staged": [...], "unstaged": [...], "untracked": [...]}
        404: {"error": "..."}
        400: {"error": "Не является git-репозиторием"}
    """
    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return jsonify({"error": "Решение не найдено"}), 404
 
    git = GitClient(solution.path)
 
    if not git.is_repo():
        return jsonify({"error": "Не является git-репозиторием"}), 400
 
    return jsonify(git.status())
 
@app.route("/api/git/commit/<name>", methods=["POST"])
def git_commit(name):
    """
    Создаёт git-коммит для решения по Conventional Commits.
 
    Body (form-data или JSON):
        type_commit  (str, обязательно) — тип: feat/fix/chore/docs/refactor/style/perf/build/test
        description  (str, обязательно) — краткое описание (заголовок коммита)
        scope        (str, необязательно) — область изменений
        body         (str, необязательно) — подробное описание
        add_all      (bool, необязательно) — если "true", выполнит git add -A перед коммитом
 
    Returns:
        200: {"ok": True, "hash": "a1b2c3d", "message": "feat(api): добавил роут"}
        400: {"error": "..."}  — валидация не прошла
        404: {"error": "Решение не найдено"}
        500: {"error": "..."}  — ошибка git
    """
    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return jsonify({"error": "Решение не найдено"}), 404
 
    # Поддержка как form-data, так и JSON
    if request.is_json:
        data = request.get_json(silent=True) or {}
        get = lambda key: data.get(key, "")
    else:
        get = lambda key: request.form.get(key, "")
 
    type_commit = get("type_commit").strip()
    description = get("description").strip()
    scope       = get("scope").strip() or None
    body        = get("body").strip() or None
    add_all     = get("add_all") in ("true", "1", "yes", True)
 
    # Базовая валидация на сервере
    if not type_commit:
        return jsonify({"error": "Поле type_commit обязательно"}), 400
    if not description:
        return jsonify({"error": "Поле description обязательно"}), 400
 
    git = GitClient(solution.path)
    result = git.commit(
        type_commit=type_commit,
        description=description,
        scope=scope,
        body=body,
        add_all=add_all,
    )
 
    if not result.ok:
        status_code = 400 if "stage" in (result.error or "") else 500
        return jsonify({"error": result.error}), status_code
 
    Logger().info(f"[GIT] commit {result.commit_hash}: {result.message}")
 
    return jsonify({
        "ok":      True,
        "hash":    result.commit_hash,
        "message": result.message,
    })
 
@app.route("/api/git/log/<name>", methods=["GET"])
def git_log(name):
    """
    Возвращает историю коммитов для решения.
 
    Query params:
        limit (int, default=10) — сколько коммитов вернуть
 
    Returns:
        200: [{"hash": str, "date": str, "author": str, "message": str}, ...]
        404: {"error": "..."}
        400: {"error": "Не является git-репозиторием"}
    """
    try:
        solution = manager.get(name)
    except FileNotFoundError:
        return jsonify({"error": "Решение не найдено"}), 404
 
    try:
        limit = int(request.args.get("limit", 10))
        limit = max(1, min(limit, 100))  # зажимаем в диапазон [1, 100]
    except ValueError:
        limit = 10
    
    git = GitClient(solution.path)
 
    if not git.is_repo():
        return jsonify({"error": "Not is git-repo"}), 400
 
    return jsonify(git.log(limit=limit))


@app.route('/api/ping', methods=['POST'])
def ping():
    """Endpoin, where frontend will send signals"""
    global LAST_HEARTBEAT
    LAST_HEARTBEAT = time.time()
    return jsonify({"status": "ok"})

@app.route("/api/solutions/<name>")
def api_solution(name):
    try:
        s = manager.get(name)
        return jsonify({
            "name": s.Name,
            "description": s.Description,
            "configuration": s.Configuration,
            "files": s.list_sources(),
        })
    except FileNotFoundError:
        return jsonify({"error": "Not found"}), 404


@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 errors for non-existent pages.
    
    This error handler is triggered when a user navigates to a URL that
    doesn't match any defined route in the application.
    
    Args:
        error: The HTTP exception object containing error details.
    
    Returns:
        tuple: A tuple containing the rendered 404 error template and
               the HTTP status code 404.
    """
    return render_template("errors/404.html", error=error), 404

if __name__ == "__main__":

    try:
        if cfg["WATCHDOG_ENABLED"] == True:
            threading.Thread(target=watchdog, daemon=True).start() # launc watchdog thread
        app.run(host=cfg["START_OPTIONS"]["host"], port=cfg["START_OPTIONS"]["port"], debug=cfg["DEBUG_MODE"])
    except Exception as e:
        Logger().error(f"[ERROR] {e}")