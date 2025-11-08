# Spark
Spark — the CLI tool that sparks your projects to life. Quickly generate project structures, scaffold files, and keep your codebase organized—so you can focus on building, not setting up.

Spark is a lightweight, opinionated CLI for bootstrapping, organizing, and managing small-to-medium code projects with minimal friction. It focuses on predictable project layouts, repeatable scaffolding, and fast iterative workflows so developers spend less time on setup and more time building.

## Key features
- Deterministic scaffolding: create consistent project structures from reusable templates.
- Context-aware commands: commands operate relative to a selected project (via `hover`) to prevent accidental cross-project changes.
- File-level operations: add, list, and remove files or directories with simple flags for common workflows.
- Editor integration: open the current project in VS Code with a single command.
- Lightweight metadata: each project includes a README and minimal metadata to allow safe tooling and automation.

## How it works (high level)
- Projects live under `solutions/` and are identified by name. Selecting a project with `hover` sets the command context.
- Templates are simple directory trees with placeholders; `new` copies a template and performs basic substitutions (e.g., project name).
- CLI operations are implemented as small, focused commands that validate inputs, report clear errors, and avoid destructive defaults.

## Templates & scaffolding
- Templates can include optional hooks (pre/post) for initializing dependencies or running generators.
- Template variables support common substitutions (project name, language, license), enabling consistent multi-language scaffolds.
- Keep templates small and composable—prefer focused templates (library, app, test harness) that can be combined.

## Extensibility and safety
- Designed to be extended via new templates or wrapper scripts; avoid adding heavy runtime dependencies.
- Destructive commands require explicit flags (`-r`, `-f`) to reduce accidental data loss.
- Prefer idempotent operations (re-run scaffolds safely) and clear logging for auditability.

## Typical workflow
1. Create a project: `new my_app cpp_basic`
2. Select it: `hover my_app`
3. Add files or iterate: `add src/main.cpp "..."` / `ls`
4. Open in editor: `code`
5. Clean up when done: `rm my_app` (or `del` for finer control)

## Best practices
- Store reusable templates in version control and document required variables.
- Use `hover` consistently in scripts to minimize accidental operations on the wrong project.
- Regularly review and test pre/post hooks in templates to keep initialization deterministic.

## Commands:
# CLI Application Documentation

## Project Management Commands

### `new <project_name> <template>`
Creates a new project with specified template.
- `project_name`: Name of the new project directory
- `template`: Template to use for project initialization
    - Available templates depend on your configuration
- Example: `new my_project cpp_basic`

### `hover <project_name>`
Sets the current working project. All subsequent commands will be executed in this project's context.
- `project_name`: Name of the project to select
- Example: `hover my_project`

## File Management Commands

### `ls [project_name]`
Lists all files and directories.
- Without arguments: Lists files in current project
- With `project_name`: Lists files in specified project
- Color coding:
    - Cyan: Directories
    - White: Files
- Example: `ls` or `ls my_project`

### `add <file_name> <content>`
Creates a new file with specified content in current project.
- `file_name`: Path/name of the file to create
- `content`: Content to write in the file
- Example: `add ./main.cpp "int main() { return 0; }"`

### `del <path> <flag>`
Deletes files or directories with specified flags:
- Flags:
    - `-r`: Recursively removes directory and all its contents
    - `-f`: Removes a single file
- Examples:
    - `del my_project -r` (removes entire project)
    - `del main.cpp -f` (removes single file)

### `rm <project_name>`
Removes an entire project directory and all its contents.
- `project_name`: Name of the project to remove
- Use `.` to remove current project
- Example: `rm my_project`

## Utility Commands

### `help`
Displays a list of available commands grouped by category:
- Project management commands
- File management commands
- Utility commands

### `echo <message>`
Prints a message to the console.
- `message`: Text to display
- Example: `echo Hello World`

### `cls`
Clears the console screen.
- Works cross-platform (Windows/Unix)

### `code`
Opens the current project in Visual Studio Code.
- Requires Visual Studio Code to be installed
- Must have a project selected via `hover`
- Example: `code`

### `exit`
Terminates the CLI application.

## General Notes

- The prompt shows the current project name in green
- Use the `hover` command before working with project-specific commands
- All projects are created in the `solutions/` directory
- Each project automatically gets a README.md file
