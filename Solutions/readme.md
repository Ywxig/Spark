# Solutions

This folder stores all solutions managed by the application. Each solution is a folder with source code and a small config file.

Do not edit anything here manually — the application handles everything for you.

## Structure

```
Solutions/
└── My Solution/
    ├── config.json   — name and description of the solution
    └── src/          — source code files
```

## config.json

```json
{
    "Name": "MyAlgo",
    "Description": "Пример решения",
    "Configuration": {
        "language": "python",
        "version": "1.0",
        "author": "me"
    }
}
```

This file is created automatically when you add a new solution.

## Important

- Do not rename, move or delete folders here manually
- All changes should be made through the application
- If you want to import existing folders as solutions, use the [Migrations](../Migrations/README.md) utility