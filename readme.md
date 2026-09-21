# SolutionD

Консольная утилита для быстрого создания проектов на основе JSON-шаблонов.

---

## Оглавление

1. [Идея](#1-идея)
2. [Структура проекта](#2-структура-проекта)
3. [Шаблон](#3-шаблон)
4. [Жизненный цикл Solution](#4-жизненный-цикл-solution)
5. [API](#5-api)
6. [Код](#6-код)
7. [Запуск и использование](#7-запуск-и-использование)
8. [Ошибки](#8-ошибки)

---

## 1. Идея

Вместо ручного создания структуры проекта пользователь выбирает шаблон, указывает имя решения — SolutionD создаёт всё остальное.

```
Шаблон → SolutionD → Готовое решение
```

---

## 2. Структура проекта

```
SolutionD/
├── config.json          # глобальная конфигурация программы
├── Templates/
│   ├── cpp-basic.json
│   └── ...
└── Solutions/           # создаваемые решения (путь из config.json)
    └── MyProject/
        ├── config.json  # конфигурация конкретного решения
        └── _src_/
            ├── main.cpp
            └── ...
```

Глобальный `config.json`:

```json
{
    "SOLUTION_DIR": "Solutions",
    "TEMPLATES_DIR": "Templates"
}
```

`_src_` — рабочая директория решения. Все операции с файлами и папками выполняются строго внутри неё.

---

## 3. Шаблон

Шаблон — JSON-файл в `Templates/`. Описывает структуру и содержимое создаваемого проекта.

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
            "ctx": "#include <iostream>\n\nint main() {\n    std::cout << \"hello world\" << std::endl;\n    return 0;\n}"
        },
        {
            "name": "include/utils.hpp",
            "ctx": "#pragma once"
        }
    ]
}
```

### Секции шаблона

| Секция | Назначение |
|---|---|
| `name` | Название шаблона |
| `description` | Описание шаблона |
| `CONFIGURATION` | Настройки решения, переносятся в `config.json` |
| `TREE` | Структура файлов и директорий |
| `FILES` | Содержимое файлов |

### TREE

Узел дерева — директория, лист (`{}`) — файл:

```json
"TREE": {
    "main.cpp": {},        // файл
    "src": {               // директория
        "utils.cpp": {}    // файл внутри src/
    }
}
```

### FILES

Каждый элемент содержит путь относительно `_src_` и содержимое файла:

```json
{
    "name": "src/utils.cpp",
    "ctx": "// utils"
}
```

Порядок работы: `TREE` создаёт структуру (пустые файлы и директории), `FILES` заполняет файлы содержимым.

---

## 4. Жизненный цикл Solution

```
Solution solution("MyProject")
        │
        ▼
solution.create()
        │
        ├── создать Solutions/MyProject/
        └── создать Solutions/MyProject/_src_/
        │
        ▼
solution.loadTemplate("cpp-basic.json")
        │
        └── загрузить Templates/cpp-basic.json в память
        │
        ▼
solution.build()
        │
        ├── TREE   → создать структуру директорий и пустые файлы
        ├── FILES  → записать содержимое в файлы
        └── CONFIGURATION → создать config.json решения
```

---

## 5. API

```cpp
class Solution {
public:
    explicit Solution(const std::string& name);

    void create();
    void loadTemplate(const std::string& filename);
    void build();

    void createDirectory(const std::string& path);
    void createFile(const std::string& path, const std::string& content);
};
```

| Метод | Описание |
|---|---|
| `Solution(name)` | Принимает имя решения, загружает глобальный конфиг |
| `create()` | Создаёт `<SOLUTION_DIR>/<name>/_src_/` |
| `loadTemplate(filename)` | Загружает шаблон из `Templates/<filename>` |
| `build()` | Разворачивает шаблон: TREE + FILES + config.json |
| `createDirectory(path)` | Создаёт директорию внутри `_src_` |
| `createFile(path, content)` | Создаёт файл с содержимым внутри `_src_` |

---

## 6. Код

### `solutions.hpp`

```cpp
#pragma once
#include <string>
#include <filesystem>
#include "../includes/json.hpp"

class Solution {
private:
    std::string name;
    nlohmann::json app_config;
    nlohmann::json tmpl;

    nlohmann::json load_app_config();
    std::filesystem::path src_path() const;
    std::filesystem::path safe_path(const std::filesystem::path& base,
                                    const std::string& relative) const;
    void build_tree(const nlohmann::json& tree, const std::filesystem::path& base);

public:
    explicit Solution(const std::string& name);

    void create();
    void loadTemplate(const std::string& filename);
    void build();
    void createDirectory(const std::string& path);
    void createFile(const std::string& path, const std::string& content);
};
```

### `solutions.cpp`

```cpp
#include "solutions.hpp"
#include <iostream>
#include <fstream>
#include <stdexcept>

using json = nlohmann::json;
namespace fs = std::filesystem;

// Загрузка глобальной конфигурации программы
json Solution::load_app_config() {
    std::ifstream file("config.json");
    if (!file.is_open())
        throw std::runtime_error("CONFIG_NOT_FOUND");

    json cfg;
    try {
        file >> cfg;
    } catch (const json::parse_error&) {
        throw std::runtime_error("CONFIG_PARSE_ERROR");
    }

    if (cfg.empty())
        throw std::runtime_error("CONFIG_IS_EMPTY");

    return cfg;
}

// Путь к рабочей директории решения
fs::path Solution::src_path() const {
    return fs::path(app_config["SOLUTION_DIR"].get<std::string>()) / name / "_src_";
}

// Проверка, что путь не выходит за пределы base
fs::path Solution::safe_path(const fs::path& base, const std::string& relative) const {
    fs::path result = fs::weakly_canonical(base / relative);
    fs::path canonical_base = fs::weakly_canonical(base);

    auto [a, b] = std::mismatch(
        canonical_base.begin(), canonical_base.end(),
        result.begin()
    );

    if (a != canonical_base.end())
        throw std::runtime_error("ERROR_PATH_IS_NOT_CORRECT");

    return result;
}

// Конструктор
Solution::Solution(const std::string& name) {
    app_config = load_app_config();

    fs::path p(name);
    if (p.filename() != p || name.empty())
        throw std::runtime_error("ERROR_NAME_IS_NOT_CORRECT");

    this->name = name;
}

// Создание структуры решения
void Solution::create() {
    if (!app_config.contains("SOLUTION_DIR") || !app_config["SOLUTION_DIR"].is_string())
        throw std::runtime_error("CONFIG_MISSING_SOLUTION_DIR");

    fs::path solution_path = fs::path(app_config["SOLUTION_DIR"].get<std::string>()) / name;

    if (fs::exists(solution_path))
        throw std::runtime_error("ERROR_SOLUTION_ALREADY_EXISTS");

    fs::create_directories(src_path());
}

// Загрузка шаблона
void Solution::loadTemplate(const std::string& filename) {
    fs::path tmpl_path = fs::path(app_config["TEMPLATES_DIR"].get<std::string>()) / filename;

    if (!fs::exists(tmpl_path))
        throw std::runtime_error("ERROR_TEMPLATE_NOT_FOUND");

    std::ifstream file(tmpl_path);
    try {
        file >> tmpl;
    } catch (const json::parse_error&) {
        throw std::runtime_error("ERROR_TEMPLATE_PARSE_ERROR");
    }
}

// Рекурсивный обход TREE
void Solution::build_tree(const json& tree, const fs::path& base) {
    for (auto& [key, value] : tree.items()) {
        fs::path current = base / key;

        if (value.empty()) {
            // Лист — файл
            fs::create_directories(current.parent_path());
            if (!fs::exists(current))
                std::ofstream f(current);
        } else {
            // Узел — директория
            fs::create_directories(current);
            build_tree(value, current);
        }
    }
}

// Сборка решения из шаблона
void Solution::build() {
    if (tmpl.empty())
        throw std::runtime_error("ERROR_TEMPLATE_NOT_LOADED");

    fs::path src = src_path();

    // 1. Структура из TREE
    if (tmpl.contains("TREE"))
        build_tree(tmpl["TREE"], src);

    // 2. Содержимое файлов из FILES
    if (tmpl.contains("FILES")) {
        for (auto& entry : tmpl["FILES"]) {
            std::string rel = entry["name"].get<std::string>();
            std::string ctx = entry.value("ctx", "");

            fs::path target = safe_path(src, rel);

            if (!fs::exists(target))
                throw std::runtime_error("ERROR_FILE_NOT_IN_TREE");

            std::ofstream f(target);
            f << ctx;
        }
    }

    // 3. config.json решения (всё кроме TREE и FILES)
    json solution_config;
    for (auto& [key, value] : tmpl.items()) {
        if (key != "TREE" && key != "FILES")
            solution_config[key] = value;
    }

    fs::path config_path = fs::path(app_config["SOLUTION_DIR"].get<std::string>()) / name / "config.json";
    std::ofstream cfg_file(config_path);
    cfg_file << solution_config.dump(4);
}

// Создание директории внутри _src_
void Solution::createDirectory(const std::string& path) {
    fs::path target = safe_path(src_path(), path);

    if (fs::exists(target))
        throw std::runtime_error("ERROR_DIRECTORY_ALREADY_EXISTS");

    fs::create_directories(target);
}

// Создание файла внутри _src_
void Solution::createFile(const std::string& path, const std::string& content) {
    fs::path target = safe_path(src_path(), path);

    if (fs::exists(target))
        throw std::runtime_error("ERROR_FILE_ALREADY_EXISTS");

    fs::create_directories(target.parent_path());

    std::ofstream f(target);
    f << content;
}
```

---

## 7. Запуск и использование

### Сборка

```bash
g++ -std=c++17 main.cpp src/solutions.cpp -o solutiond
```
или
```bash
make run
```

### CLI

#### Создание решения
```bash
# Создать решение из шаблона
./solutiond create MyProject --template cpp-basic.json

# Создать решение из другого шаблона
./solutiond create WebApp --template html-basic.json
```
#### Открыть в редакторе
что бы открыть решение в редакторе необходимо использовтаь комманду open <имя решения>

```bash
./solutiond open MyProject
```

### Использование в коде

```cpp
#include "src/solutions.hpp"
#include <iostream>

int main() {
    try {
        Solution solution("MyProject");
        solution.create();
        solution.loadTemplate("cpp-basic.json");
        solution.build();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
```

### Результат

После выполнения команды:

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

### Ручное управление файлами

```cpp
Solution solution("MyProject");
solution.create();

// Создать директорию вручную
solution.createDirectory("core/utils");

// Создать файл вручную
solution.createFile("core/utils/math.cpp", "int add(int a, int b) { return a + b; }");
```

---

## 8. Ошибки

| Код | Причина |
|---|---|
| `ERROR_NAME_IS_NOT_CORRECT` | Имя содержит `/`, `..` или является путём |
| `ERROR_SOLUTION_ALREADY_EXISTS` | Директория решения уже существует |
| `ERROR_PATH_IS_NOT_CORRECT` | Путь выходит за пределы `_src_` |
| `ERROR_FILE_ALREADY_EXISTS` | Файл уже существует |
| `ERROR_DIRECTORY_ALREADY_EXISTS` | Директория уже существует |
| `ERROR_TEMPLATE_NOT_FOUND` | Файл шаблона не найден в `Templates/` |
| `CONFIG_NOT_FOUND` | Не найден глобальный `config.json` |
