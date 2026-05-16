# Spark

A local web application for managing personal code solutions. Spark gives you a clean UI to create, browse, and open coding solutions — with migration support, IDE integration, and Markdown readme rendering.

---

## Features

- **Solution management** — create, view, and delete named solutions with descriptions
- **Source file browser** — list and inspect files inside each solution's source directory
- **Readme rendering** — Markdown `readme.md` auto-rendered on the solution detail page
- **Templates** — create solutions from predefined code templates
- **Migrations** — import solutions from a migrations directory in bulk
- **IDE integration** — open any solution directly in your editor (e.g. VS Code) with one click
- **REST API** — JSON endpoints for listing and inspecting solutions
- **Configurable** — all paths, ports, author info, and IDE settings controlled from `config.json`

---

## Getting Started

### Requirements

- Python 3.10+
- pip

### Install

```bash
git clone https://github.com/Ywxig/Spark.git
cd Spark
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

The app starts at `http://127.0.0.1:5000` by default. Set `open_in_browser: true` in `config.json` to open it automatically.

---

## Configuration

All settings live in `config.json` at the project root.

```json
{
    "SOLUTION_DIR": "Solutions",
    "APP_NAME": "Spark",
    "SRC_DIR": "_src_",
    "CONFIG_FILE": "config.json",
    "MIGRATION_DIR": "Migrations",
    "CODE_TEMPLATE_DIR": "Code/.templates/",
    "DEBUG_MODE": true,

    "LOG": {
        "LEVEL": "INFO",
        "FILE": "app.log"
    },

    "AUTHOR": {
        "NAME": "SomeUser",
        "AVATAR": "../static/avatars/avatar.png",
        "GITHUB": "https://github.com/",
        "LANGUAGE": "en",
        "EMAIL": "",
        "LINKS": []
    },

    "START_OPTIONS": {
        "open_in_browser": false,
        "check_open_in_browser": true,
        "port": 5000,
        "host": "127.0.0.1"
    },

    "IDE": {
        "open_in_ide": true,
        "open_in_ide_cmd": true,
        "name": "Visual Studio Code",
        "path": "",
        "cmd": {
            "open": "code"
        }
    }
}
```

| Key | Description |
|---|---|
| `SOLUTION_DIR` | Folder where solutions are stored |
| `SRC_DIR` | Source subdirectory name inside each solution |
| `MIGRATION_DIR` | Folder scanned when running migrations |
| `CODE_TEMPLATE_DIR` | Folder containing solution templates |
| `DEBUG_MODE` | Enable Flask debug mode and hot-reload |
| `IDE.cmd.open` | Shell command to open the editor (e.g. `code`, `subl`) |
| `IDE.path` | Absolute path to the editor binary; leave empty to use PATH |
| `START_OPTIONS.open_in_browser` | Auto-open browser on startup |

---

## Project Structure

```
Spark/
├── main.py                  # Flask app, all routes
├── config.json              # User configuration
├── config_loader.py         # Config read/write
├── Solutions/               # Created solutions live here
├── Migrations/              # Migration sources
├── src/
│   ├── Solution_Manager/    # Core logic: create, get, delete, list
│   │   └── template.py      # Template support
│   └── loger.py             # Logger wrapper
└── templates/
    ├── base.html
    ├── index.html
    ├── detail.html
    ├── create.html
    ├── migration.html
    ├── option.html
    ├── user.html
    ├── docs/
    └── errors/
```

---

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | List all solutions |
| GET/POST | `/create` | Create a new solution |
| GET | `/solution/<name>` | Solution detail with file tree and readme |
| POST | `/solution/<name>/delete` | Delete a solution |
| POST | `/solution/<name>/open` | Open solution in IDE |
| GET/POST | `/migrate` | View available migrations |
| GET/POST | `/migrate/run` | Run migration from `MIGRATION_DIR` |
| GET/POST | `/option` | Settings panel |
| GET | `/user` | Author profile |
| GET | `/docs` | Documentation |
| GET | `/api/solutions` | JSON list of all solutions |
| GET | `/api/solutions/<name>` | JSON detail for one solution |

---

## IDE Integration

To enable one-click opening, set `IDE.open_in_ide: true` and configure your editor command:

```json
"IDE": {
    "open_in_ide": true,
    "cmd": { "open": "code" },
    "path": ""
}
```

`path` takes priority over `cmd` if set. Leave it blank to use whatever is on your system PATH. The solution's source folder (`SRC_DIR`) is passed as the argument.

---

## Migrations

Place solution folders in the directory specified by `MIGRATION_DIR`, then visit `/migrate` and click **Run**. Spark will import each folder as a solution.

---

## API

```bash
# List all solutions
GET /api/solutions

# Get a single solution
GET /api/solutions/<name>
```

Response shape:

```json
{
    "name": "my-solution",
    "description": "Some description",
    "configuration": {},
    "files": ["main.py", "readme.md"]
}
```

---

## License

MIT
