# Migrations

A simple utility to import existing solutions into `SolutionManager` in bulk.

## What it does

It scans a folder you give it. Every subfolder inside becomes a new solution — with its own `config.json` and `src/` directory. All files are copied automatically.

## Usage

```python
from src.Solution_Manager import SolutionManager
from src.Solution_Manager.migrate import migrate

manager = SolutionManager()
result = migrate(manager, source_dir="path/to/old/solutions")

print(result)
# {"migrated": 5, "skipped": 1, "failed": 0}
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `manager` | `SolutionManager` | The manager where solutions will be imported |
| `source_dir` | `str` | Path to the folder with solutions you want to import |

## Return value

A dictionary with migration results:

| Key | Description |
|---|---|
| `migrated` | Successfully imported |
| `skipped` | Already exists, so it was skipped |
| `failed` | Something went wrong during import |

## How it behaves

- If `source_dir` does not exist or is not a folder — raises `ValueError`
- If the folder is empty — returns `{"migrated": 0, "skipped": 0, "failed": 0}`
- Solutions are processed in alphabetical order
- If a solution already exists, it is skipped without any error
- All files are copied recursively into the `src/` folder of the new solution
