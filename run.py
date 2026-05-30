#!/usr/bin/env python3

import click
import os
import subprocess
import sys
from pathlib import Path

LOACTION_OF_SKRIPT = os.path.dirname(os.path.realpath(__file__))
from config_loader import ConfigLoader

CFG = ConfigLoader(f"{LOACTION_OF_SKRIPT}/config.json").load()

# ANSI colours
GREEN  = '\033[0;32m'
YELLOW = '\033[1;33m'
RED    = '\033[0;31m'
NC     = '\033[0m'

def g(msg): click.echo(f"{GREEN}{msg}{NC}")
def y(msg): click.echo(f"{YELLOW}{msg}{NC}")
def r(msg): click.echo(f"{RED}{msg}{NC}")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Spark — утилита запуска Flask-приложения."""
    # Если команда не указана — запускаем run по умолчанию
    if ctx.invoked_subcommand is None:
        ctx.invoke(version)


@cli.command()
def run():
    """Запустить Flask-приложение (аналог spark.sh)."""
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    g("=== Start Flask-app ===\n")

    venv_dir = script_dir / ".venv"
    python_bin = venv_dir / "bin" / "python"
    pip_bin    = venv_dir / "bin" / "pip"

    # ── Виртуальное окружение ──────────────────────────────────────────────
    if not venv_dir.is_dir():
        y(".venv не найден. Создаю...")
        result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        if result.returncode != 0:
            r("Ошибка: не удалось создать venv")
            sys.exit(1)

    g("Активирую venv...")

    # ── Зависимости ───────────────────────────────────────────────────────
    req = script_dir / "requirements.txt"
    if req.is_file():
        g("Проверяю зависимости...")
        subprocess.run([str(pip_bin), "install", "-q", "--upgrade", "pip"])
        result = subprocess.run([str(pip_bin), "install", "-q", "-r", str(req)])
        if result.returncode != 0:
            r("Ошибка при установке зависимостей из requirements.txt")
            sys.exit(1)
    else:
        y("Файл requirements.txt не найден")

    # ── Проверка main.py ──────────────────────────────────────────────────
    main_py = script_dir / "main.py"
    if not main_py.is_file():
        r("Файл main.py не найден!")
        sys.exit(1)

    # ── Запуск ────────────────────────────────────────────────────────────
    click.clear()
    g("=== App started ===\n")
    y("Доступно по адресу: http://127.0.0.1:8000\n")
    y("Для остановки нажмите Ctrl+C\n")
    g("=" * 40 + "\n")

    env = os.environ.copy()
    env.update({
        "FLASK_APP":   "main.py",
        "FLASK_ENV":   "development",
        "FLASK_DEBUG": "1",
    })

    try:
        subprocess.run([str(python_bin), str(main_py)], env=env, cwd=str(main_py.parent))
    except KeyboardInterrupt:
        g("\nПриложение остановлено.")

@cli.command()
def version():
    y(CFG["VERSION"])

if __name__ == "__main__":
    cli()