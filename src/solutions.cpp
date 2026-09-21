#include "solutions.hpp"
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <vector>
#include <ranges>
#include "colorise.hpp"
#include "util.hpp"

using json = nlohmann::json;
namespace fs = std::filesystem;


json Solution::load_app_config() {
    std::ifstream file(get_parent_dir_path_str() + "config.json");
    //print( get_parent_dir_path_str() + "config.json", "white" );

    if (!file.is_open())
        throw std::runtime_error("CONFIG_NOT_FOUND");

    json cfg;
    try {
        file >> cfg;
    } catch (const json::parse_error& e) {
        throw std::runtime_error("CONFIG_PARSE_ERROR");
    }

    if (cfg.empty())
        throw std::runtime_error("CONFIG_IS_EMPTY");

    return cfg;
}

/**
 * @brief Constructs and returns the filesystem path to the source directory of this solution.
 *        The path is formed by using the absolute solution directory from the application configuration
 *        and combining it with the solution's name and the fixed subdirectory "_src_".
 *
 * @return fs::path An object representing the full path to the solution's source code directory.
 */
fs::path Solution::src_path() const {
    fs::path solution_dir = app_config["SOLUTION_DIR"].get<std::string>();
    return solution_dir / name / "_src_";
}

fs::path Solution::safe_path(const fs::path& base, const std::string& relative) const {
    fs::path result = fs::weakly_canonical(base / relative);
    fs::path canonical_base = fs::weakly_canonical(base);

    // Проверяем, что result начинается с base
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

    // Имя должно быть простым — без слэшей и ".."
    fs::path p(name);
    if (p.filename() != p || name.empty())
        throw std::runtime_error("ERROR_NAME_IS_NOT_CORRECT");

    this->name = name;
}

void Solution::loadTemplate(const std::string& filename) {
    fs::path template_dir = app_config["CODE_TEMPLATE_DIR"].get<std::string>();
    fs::path tmpl_path = template_dir / filename;

    if (!fs::exists(tmpl_path))
        throw std::runtime_error("ERROR_TEMPLATE_NOT_FOUND");

    std::ifstream file(tmpl_path);
    try {
        file >> tmpl;
    } catch (const json::parse_error& e) {
        throw std::runtime_error("ERROR_TEMPLATE_PARSE_ERROR");
    }
}

// Вспомогательный рекурсивный метод для обхода TREE
void Solution::build_tree(const json& tree, const fs::path& base) {
    for (auto& [key, value] : tree.items()) {
        fs::path current = base / key;

        if (value.empty()) {
            // Лист — это файл (создаём пустым, содержимое придёт из FILES)
            fs::create_directories(current.parent_path());
            if (!fs::exists(current)) {
                std::ofstream f(current);
            }
        } else {
            // Узел — это директория
            fs::create_directories(current);
            build_tree(value, current);
        }
    }
}
void Solution::build() {
    if (tmpl.empty())
        throw std::runtime_error("ERROR_TEMPLATE_NOT_LOADED");

    fs::path src = src_path();

    // 1. Строим структуру из TREE
    if (tmpl.contains("TREE")) {
        build_tree(tmpl["TREE"], src);
    }

    // 2. Заполняем файлы содержимым из FILES
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

    // 3. Пишем config.json решения
    json solution_config;
    for (auto& [key, value] : tmpl.items()) {
        if (key != "TREE" && key != "FILES") {
            solution_config[key] = value;
        }
    }

    fs::path solution_dir = app_config["SOLUTION_DIR"].get<std::string>();
    fs::path config_path = solution_dir / name / "config.json";
    std::ofstream cfg_file(config_path);
    cfg_file << solution_config.dump(4);
}

void Solution::create() {
    if (!app_config.contains("SOLUTION_DIR") || !app_config["SOLUTION_DIR"].is_string())
        throw std::runtime_error("CONFIG_MISSING_SOLUTION_DIR");

    fs::path solution_dir = app_config["SOLUTION_DIR"].get<std::string>();
    fs::path solution_path = solution_dir / name;

    if (fs::exists(solution_path))
        throw std::runtime_error("ERROR_SOLUTION_ALREADY_EXISTS");

    fs::create_directories(src_path());
}

void Solution::open_in_ide() {
    fs::path solution_dir = app_config["SOLUTION_DIR"].get<std::string>();
    fs::path target_path = solution_dir / name / "_src_";
    std::string cmd = app_config["OPEN_IN_IDE_CMD"].get<std::string>() + " " + target_path.string();
    std::cout << cmd << std::endl;
    system(cmd.c_str());
}

std::vector<std::string> Solution::index_sons() {
    json app_config = load_app_config();

    if (!app_config.contains("SOLUTION_DIR") || !app_config["SOLUTION_DIR"].is_string()) {
        throw std::runtime_error("CONFIG_MISSING_SOLUTION_DIR");
    }

    fs::path dir_path = app_config["SOLUTION_DIR"].get<std::string>();

    std::error_code ec;
    if (!fs::exists(dir_path, ec) || !fs::is_directory(dir_path, ec)) {
        return {};
    }

    std::vector<std::string> result;
    for (const auto& entry : fs::directory_iterator(dir_path, fs::directory_options::skip_permission_denied, ec)) {
        std::error_code err;
        if (entry.is_directory(err)) {
            result.push_back(entry.path().filename().string());
        }
    }

    return result;
}

std::vector<std::string> Solution::index_tmpl() {
    json app_config = load_app_config();

    if (!app_config.contains("CODE_TEMPLATE_DIR") || !app_config["CODE_TEMPLATE_DIR"].is_string()) {
        throw std::runtime_error("CONFIG_MISSING_CODE_TEMPLATE_DIR");
    }

    fs::path dir_path = app_config["CODE_TEMPLATE_DIR"].get<std::string>();

    std::error_code ec;
    if (!fs::exists(dir_path, ec) || !fs::is_directory(dir_path, ec)) {
        return {};
    }

    std::vector<std::string> result;
    for (const auto& entry : fs::directory_iterator(dir_path, fs::directory_options::skip_permission_denied, ec)) {
        std::error_code err;
        if (entry.is_regular_file(err)) {
            result.push_back(entry.path().filename().string());
        }
    }

    return result;
}

 void Solution::delete_solution(const std::string& solution_name) {
    json app_config = load_app_config();

    if (!app_config.contains("SOLUTION_DIR") || !app_config["SOLUTION_DIR"].is_string()) {
        throw std::runtime_error("CONFIG_MISSING_SOLUTION_DIR");
    }

    fs::path dir_path = app_config["SOLUTION_DIR"].get<std::string>();

    fs::path solution_path = dir_path / solution_name;
    if (fs::exists(solution_path)) {
        fs::remove_all(solution_path);
    }
}
