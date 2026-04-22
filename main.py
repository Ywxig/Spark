"""
Flask приложение для управления решениями.
Запуск: python app.py
"""

import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.Solution_Manager import SolutionManager, Solution
from config_loader import ConfigLoader

import os

import webbrowser

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

# Страницы

@app.route("/")
def index():
    """Список всех решений."""
    solutions = manager.index()
    return render_template("index.html", solutions=solutions)

@app.route("/migrate")
def migrate():
    """Панель с настройкой миграции"""
    return render_template("migration.html")

@app.route("/user")
def user_info():
    """Statistic about user"""
    return render_template("user.html")

@app.route("/solution/<name>")
def solution_detail(name):
    """Детальная страница решения."""
    try:
        solution = manager.get(name)
        files = solution.list_sources()
        return render_template("detail.html", solution=solution, files=files)
    except FileNotFoundError:
        return render_template("404.html"), 404


@app.route("/create", methods=["GET", "POST"])
def create():
    """Создать новое решение."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            return render_template("create.html", error="Имя не может быть пустым.")

        try:
            manager.create(Name=name, Description=description)
            return redirect(url_for("solution_detail", name=name))
        except FileExistsError:
            return render_template("create.html", error=f"Решение «{name}» уже существует.")

    return render_template("create.html")


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

    cmd = ide.get("cmd", {}).get("open", "").strip()
    if not cmd:
        return jsonify({"error": "IDE.cmd.open не задан в config.json"}), 400

    # Если задан явный путь к исполняемому файлу — используем его,
    # иначе берём команду из PATH (например, "code")
    exe_path = ide.get("path", "").strip()
    executable = exe_path if exe_path else cmd

    try:
        subprocess.Popen([executable, str(solution.path)])
        return jsonify({"ok": True, "opened": str(solution.path)})
    except FileNotFoundError:
        return jsonify({"error": f"Редактор «{executable}» не найден. Проверь IDE.path в config.json"}), 500



# API (JSON)
@app.route("/api/solutions")
def api_solutions():
    solutions = manager.index()
    return jsonify([{
        "name": s.Name,
        "description": s.Description,
        "files": s.list_sources(),
    } for s in solutions])


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

if __name__ == "__main__":
    start_options = cfg["START_OPTIONS"]
    
    if start_options["open_in_browser"]:
        ip = start_options["ip"]
        port = start_options["port"]
        url = f"http://{ip}:{port}"
        
        should_open = False
        
        if not start_options["check_open_in_browser"]:
            should_open = True
        else:
            # Only open if not running as the reloader child process
            if not os.environ.get("WERKZEUG_RUN_MAIN"):
                should_open = True
        
        if should_open:
            webbrowser.open(url)
    
    # Передаем порт в параметры запуска
    app.run(host=cfg["START_OPTIONS"]["ip"], port=cfg["START_OPTIONS"]["port"], debug=True)