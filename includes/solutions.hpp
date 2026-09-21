#pragma once

#include <string>
#include <filesystem>
#include <vector>
#include "../includes/json.hpp"

class Solution {
private:
    std::string name;
    nlohmann::json app_config;   // config.json программы (SOLUTION_DIR и т.д.)
    nlohmann::json tmpl;         // загруженный шаблон

    std::filesystem::path src_path() const; // <SOLUTION_DIR>/<name>/_src_
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
    void open_in_ide();
    static void delete_solution(const std::string& solution_name);

    // Статические методы для работы без создания объекта класса:
    static nlohmann::json load_app_config();
    static std::vector<std::string> index_sons();
    static std::vector<std::string> index_tmpl();
};
