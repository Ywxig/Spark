# Spark
Spark — the CLI tool that sparks your projects to life. Quickly generate project structures, scaffold files, and keep your codebase organized—so you can focus on building, not setting up.

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