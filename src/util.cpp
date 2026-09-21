#include "util.hpp"
#include <stdexcept>

fs::path get_executable_path() {
    std::error_code ec;
    fs::path exe_path = fs::canonical("/proc/self/exe", ec);

    if (ec) {
        throw std::runtime_error("Не удалось получить путь к исполняемому файлу: " + ec.message());
    }

    return exe_path;
}

fs::path get_config_path() {
    return get_executable_path().parent_path() / "config.json";
}

fs::path get_executable_dir() {
    return get_executable_path().parent_path();
}

// Реализации для совпадения с вызовами в solutions.cpp
fs::path get_parent_dir_path() {
    return get_executable_dir();
}

std::string get_parent_dir_path_str() {
    return get_executable_dir().string() + "/";
}