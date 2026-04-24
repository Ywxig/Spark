from git import Repo

class GitClient:
    def __init__(self, repo_path: str) -> None:
        self.repo = Repo(repo_path)

    def create(self):
        """
        Create a new git repository in the given path.
        """
        self.repo.init()

    
    def commit_and_push(self, content: dict) -> None:
        """
        content -> {
            "type": "feat",
            "subject": "Added a new feature",
            "description": "This is a long description of the feature"
        }
        """
        self.repo.git.add(".")

        """
        Changes relevant to the API or UI:

            feat Commits that add, adjust or remove a feature to/of/from the API or UI
            fix Commits that fix an API or UI bug of a preceded feat commit

        refactor Commits that rewrite or restructure code without altering API or UI behavior

            perf Commits are special type of refactor commits that specifically improve performance

        style Commits that address code style (e.g., white-space, formatting, missing semi-colons) and do not affect application behavior
        test Commits that add missing tests or correct existing ones
        docs Commits that exclusively affect documentation
        build Commits that affect build-related components such as build tools, dependencies, project version, ...
        ops Commits that affect operational aspects like infrastructure (IaC), deployment scripts, CI/CD pipelines, backups, monitoring, or recovery procedures, ...
        chore Commits that represent tasks like initial commit, modifying .gitignore, ...
        """



        self.repo.git.commit("-m", f"{content['type']} {content['subject']}: {content['description']}")
        self.repo.git.push()