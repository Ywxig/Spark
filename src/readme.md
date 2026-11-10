# SolutionD

Консольная утилита для создания проектов по JSON-шаблонам.

```
Шаблон → SolutionD → готовое решение
```

## Структура проекта

```
SolutionD/
├── main.cpp                 # CLI: разбор команд и их выполнение
├── Makefile
├── Templates/               # JSON-шаблоны
├── src/
│   ├── solutions.cpp        # работа с решениями и шаблонами
│   ├── colorise.cpp         # раскраска вывода
│   ├── config.json          # конфигурация приложения
│   └── includes/
│       ├── solutions.hpp
│       ├── colorise.hpp
│       └── json.hpp
└── dist/                    # результат сборки
```

## Конфигурация

`config.json` лежит рядом с исполняемым файлом (в `dist/` после сборки):

```json
{
    "SOLUTION_DIR": "/path/to/Solutions",
    "CODE_TEMPLATE_DIR": "/path/to/Templates",
    "OPEN_IN_IDE_CMD": "dev.zed.Zed"
}
```

| Поле | Назначение |
|---|---|
| `SOLUTION_DIR` | Каталог, в котором создаются решения |
| `CODE_TEMPLATE_DIR` | Каталог с JSON-шаблонами |
| `OPEN_IN_IDE_CMD` | Команда открытия решения в редакторе |

## Шаблон

```json
{
    "name": "C++ Basic",
    "description": "Minimal C++ project",

    "CONFIGURATION": {
        "language": "cpp",
        "version": "1.0",
        "author": ""
    },

    "TREE": {
        "main.cpp": {},
        "include": {
            "utils.hpp": {}
        },
        "src": {
            "utils.cpp": {}
        }
    },

    "FILES": [
        {
            "name": "main.cpp",
            "ctx": "#include <iostream>\n\nint main() {\n    return 0;\n}"
        }
    ]
}
```

- `TREE` создаёт структуру. Объект — каталог, пустой объект `{}` — файл.
- `FILES` заполняет файлы содержимым. Путь указывается относительно `_src_`.
- Все секции, кроме `TREE` и `FILES`, попадают в `config.json` решения.

## Использование

```bash
make            # собрать проект
./dist/main     # показать справку
```

| Команда | Действие |
|---|---|
| `./dist/main open <name>` | Открыть решение в IDE |
| `./dist/main ls` | Показать решения |
| `./dist/main ls t` | Показать шаблоны |
| `./dist/main create <name> <template>` | Создать решение |
| `./dist/main del <name>` | Удалить решение |

Пример:

```bash
./dist/main create MyProject cpp_basic.json
```

Результат:

```
Solutions/
└── MyProject/
    ├── config.json
    └── _src_/
        ├── main.cpp
        ├── include/
        │   └── utils.hpp
        └── src/
            └── utils.cpp
```

## API

Код построен в процедурном стиле: состояние передаётся через `AppConfig`, а действия выполняют свободные функции.

```cpp
struct AppConfig {
    std::filesystem::path solutions_dir;
    std::filesystem::path templates_dir;
    std::string open_cmd;
};

AppConfig load_app_config();

std::vector<std::string> list_solutions(const AppConfig& config);
std::vector<std::string> list_templates(const AppConfig& config);

std::string solution_description(const AppConfig& config, const std::string& name);
std::string template_description(const AppConfig& config, const std::string& name);

void create_solution(const AppConfig& config, const std::string& name, const std::string& template_name);
void open_solution(const AppConfig& config, const std::string& name);
void delete_solution(const AppConfig& config, const std::string& name);
```

Все CLI-команды реализованы прямо в `main()`. Отдельных обработчиков (`handlers`) нет.

## Ошибки

| Код | Причина |
|---|---|
| `CONFIG_NOT_FOUND` | Не найден `config.json` рядом с исполняемым файлом |
| `CONFIG_PARSE_ERROR` | Ошибка разбора `config.json` |
| `CONFIG_IS_EMPTY` | Пустой `config.json` |
| `CONFIG_MISSING_SOLUTION_DIR` | Нет поля `SOLUTION_DIR` |
| `CONFIG_MISSING_CODE_TEMPLATE_DIR` | Нет поля `CODE_TEMPLATE_DIR` |
| `ERROR_NAME_IS_NOT_CORRECT` | Имя решения содержит путь или пустое |
| `ERROR_TEMPLATE_NOT_FOUND` | Шаблон не найден |
| `ERROR_TEMPLATE_PARSE_ERROR` | Ошибка разбора шаблона |
| `ERROR_SOLUTION_ALREADY_EXISTS` | Решение уже существует |
| `ERROR_FILE_NOT_IN_TREE` | Файл из `FILES` отсутствует в `TREE` |
| `ERROR_PATH_IS_NOT_CORRECT` | Путь выходит за пределы `_src_` |
