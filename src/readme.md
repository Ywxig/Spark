# src

This is the source code directory of the application.

## Structure

```
src/
└── Solution_Manager/
    ├── __init__.py    — exports Solution and SolutionManager
    ├── solution.py    — Solution class
    ├── manager.py     — SolutionManager class
    └── migrate.py     — migration utility
```

## Modules

**`Solution_Manager`** is the core module of the application. It handles everything related to solutions — creating, reading, updating, and deleting them.

| File | Description |
|---|---|
| `solution.py` | Represents a single solution. Reads and writes its `config.json` and manages files in `src/` |
| `manager.py` | Creates, deletes, and lists solutions. All solutions are stored in the `Solutions/` folder |
| `migrate.py` | Imports existing folders into the application as solutions |
