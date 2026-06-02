"""
Git-клиент для управления репозиторием.
Размести этот файл по пути: src/git_client.py
"""

import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class CommitResult:
    ok: bool
    message: str
    commit_hash: Optional[str] = None
    error: Optional[str] = None


class GitClient:
    """
    Клиент для работы с git-репозиторием.

    Args:
        repo_path: Путь к корню репозитория. По умолчанию — текущая директория.

    Example:
        git = GitClient("/path/to/repo")
        result = git.commit("feat", "добавил новый роут", scope="api")
    """

    def __init__(self, repo_path: str | Path = "."):
        self.repo_path = Path(repo_path).resolve()

    # ------------------------------------------------------------------ #
    #  Внутренние хелперы                                                  #
    # ------------------------------------------------------------------ #

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        """Запускает git-команду в repo_path и возвращает результат."""
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

    # ------------------------------------------------------------------ #
    #  Публичные методы                                                    #
    # ------------------------------------------------------------------ #

    def is_repo(self) -> bool:
        """Проверяет, является ли repo_path git-репозиторием."""
        result = self._run("rev-parse", "--is-inside-work-tree")
        return result.returncode == 0

    def current_branch(self) -> str:
        """Возвращает имя текущей ветки."""
        result = self._run("rev-parse", "--abbrev-ref", "HEAD")
        if result.returncode == 0:
            return result.stdout.strip()
        return "unknown"

    def staged_files(self) -> list[str]:
        """Возвращает список файлов, добавленных в stage (git add)."""
        result = self._run("diff", "--cached", "--name-only")
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().splitlines()
        return []

    def status(self) -> dict:
        """
        Возвращает краткий статус репозитория.

        Returns:
            dict: {
                "branch": str,
                "staged": list[str],
                "unstaged": list[str],
                "untracked": list[str],
            }
        """
        staged = self.staged_files()

        # Изменённые, но не в stage
        unstaged_result = self._run("diff", "--name-only")
        unstaged = unstaged_result.stdout.strip().splitlines() if unstaged_result.returncode == 0 else []

        # Неотслеживаемые файлы
        untracked_result = self._run("ls-files", "--others", "--exclude-standard")
        untracked = untracked_result.stdout.strip().splitlines() if untracked_result.returncode == 0 else []

        return {
            "branch": self.current_branch(),
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
        }

    def build_message(
        self,
        type_commit: str,
        description: str,
        scope: Optional[str] = None,
        body: Optional[str] = None,
    ) -> str:
        """
        Собирает сообщение коммита по Conventional Commits.

        Format:
            <type>(<scope>): <description>

            <body>

        Args:
            type_commit: Тип (feat, fix, chore, docs, refactor, style, perf, build, test).
            description: Краткое описание изменений (заголовок).
            scope:       Область изменений (необязательно).
            body:        Подробное описание (необязательно).

        Returns:
            Готовое сообщение коммита.
        """
        scope_part = f"({scope.strip()})" if scope and scope.strip() else ""
        header = f"{type_commit.strip()}{scope_part}: {description.strip()}"

        if body and body.strip():
            return f"{header}\n\n{body.strip()}"
        return header

    def commit(
        self,
        type_commit: str,
        description: str,
        scope: Optional[str] = None,
        body: Optional[str] = None,
        add_all: bool = False,
    ) -> CommitResult:
        """
        Создаёт коммит в репозитории.

        Args:
            type_commit: Тип коммита (feat, fix, chore …).
            description: Краткое описание.
            scope:       Область изменений (необязательно).
            body:        Подробное описание (необязательно).
            add_all:     Если True — перед коммитом выполнит `git add -A`.

        Returns:
            CommitResult с полями ok, message, commit_hash, error.
        """
        if not self.is_repo():
            return CommitResult(ok=False, message="", error="Не является git-репозиторием")

        if not description.strip():
            return CommitResult(ok=False, message="", error="Описание коммита не может быть пустым")

        valid_types = {"feat", "fix", "chore", "docs", "refactor", "style", "perf", "build", "test"}
        if type_commit not in valid_types:
            return CommitResult(
                ok=False,
                message="",
                error=f"Неизвестный тип коммита: «{type_commit}». Допустимые: {', '.join(sorted(valid_types))}",
            )

        if add_all:
            add_result = self._run("add", "-A")
            if add_result.returncode != 0:
                return CommitResult(ok=False, message="", error=f"git add -A завершился с ошибкой: {add_result.stderr}")

        # Проверяем, есть ли что коммитить
        if not self.staged_files():
            return CommitResult(ok=False, message="", error="Нет файлов в stage. Выполни git add перед коммитом.")

        msg = self.build_message(type_commit, description, scope, body)

        result = self._run("commit", "-m", msg)

        if result.returncode != 0:
            return CommitResult(ok=False, message=msg, error=result.stderr.strip())

        # Получаем хэш последнего коммита
        hash_result = self._run("rev-parse", "--short", "HEAD")
        commit_hash = hash_result.stdout.strip() if hash_result.returncode == 0 else None

        return CommitResult(ok=True, message=msg, commit_hash=commit_hash)

    def log(self, limit: int = 10) -> list[dict]:
        """
        Возвращает последние коммиты из истории.

        Args:
            limit: Сколько коммитов вернуть (по умолчанию 10).

        Returns:
            Список словарей: [{"hash": str, "date": str, "author": str, "message": str}]
        """
        fmt = "%h|%ai|%an|%s"
        result = self._run("log", f"-{limit}", f"--pretty=format:{fmt}")
        if result.returncode != 0 or not result.stdout.strip():
            return []

        commits = []
        for line in result.stdout.strip().splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append({
                    "hash":    parts[0],
                    "date":    parts[1],
                    "author":  parts[2],
                    "message": parts[3],
                })
        return commits