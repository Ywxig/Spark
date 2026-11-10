#pragma once

#include <filesystem>
#include <string>
#include <vector>
#include "json.hpp"

// Настройки приложения из config.json рядом с исполняемым файлом.
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
