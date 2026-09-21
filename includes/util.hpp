#pragma once

#include <filesystem>
#include <string>

namespace fs = std::filesystem;

fs::path get_executable_path();
fs::path get_config_path();
fs::path get_executable_dir();

// Старые функции для обратной совместимости с solutions.cpp
fs::path get_parent_dir_path();
std::string get_parent_dir_path_str();