#include "includes/solutions.hpp"

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>

#include "includes/colorise.hpp"

namespace fs = std::filesystem;
using json = nlohmann::json;

namespace Config {

    fs::path executable_dir() {
        std::error_code ec;
        fs::path exe = fs::canonical("/proc/self/exe", ec);
        if (ec)
            throw std::runtime_error("ERROR_EXECUTABLE_PATH");
        return exe.parent_path();
    }

    json read_json(const fs::path& path, const char* not_found_error, const char* parse_error) {
        std::ifstream file(path);
        if (!file)
            throw std::runtime_error(not_found_error);

        json data;
        try {
            file >> data;
        } catch (const json::parse_error&) {
            throw std::runtime_error(parse_error);
        }
        return data;
    }

    void validate_name(const std::string& name) {
        fs::path path(name);
        if (name.empty() || path.filename() != path)
            throw std::runtime_error("ERROR_NAME_IS_NOT_CORRECT");
    }

    fs::path solution_dir(const AppConfig& config, const std::string& name) {
        validate_name(name);
        return config.solutions_dir / name;
    }

    fs::path safe_path(const fs::path& base, const std::string& relative) {
        fs::path result = fs::weakly_canonical(base / relative);
        fs::path root = fs::weakly_canonical(base);

        auto mismatch = std::mismatch(root.begin(), root.end(), result.begin());
        if (mismatch.first != root.end())
            throw std::runtime_error("ERROR_PATH_IS_NOT_CORRECT");

        return result;
    }

    void build_tree(const json& tree, const fs::path& base) {
        for (const auto& [name, node] : tree.items()) {
            fs::path current = base / name;

            if (node.empty()) {
                fs::create_directories(current.parent_path());
                std::ofstream file(current);
            } else {
                fs::create_directories(current);
                build_tree(node, current);
            }
        }
    }

    std::vector<std::string> list_entries(const fs::path& dir, bool directories) {
        std::error_code ec;
        if (!fs::is_directory(dir, ec))
            return {};

        std::vector<std::string> names;
        for (const auto& entry : fs::directory_iterator(dir, fs::directory_options::skip_permission_denied, ec)) {
            std::error_code entry_error;
            bool matches = directories ? entry.is_directory(entry_error) : entry.is_regular_file(entry_error);
            if (matches)
                names.push_back(entry.path().filename().string());
        }

        std::sort(names.begin(), names.end());
        return names;
    }

    std::string read_description(const fs::path& path, const char* key, const char* not_found) {
        if (!fs::exists(path))
            return not_found;

        try {
            std::ifstream file(path);
            json data;
            file >> data;

            if (data.contains(key) && data[key].is_string())
                return data[key].get<std::string>();
            return "No description";
        } catch (const std::exception&) {
            return "Error parsing description";
        }
    }

} // namespace

using namespace Config;

AppConfig load_app_config() {
    json data = read_json(executable_dir() / "config.json", "CONFIG_NOT_FOUND", "CONFIG_PARSE_ERROR");
    if (data.empty())
        throw std::runtime_error("CONFIG_IS_EMPTY");

    if (!data.contains("SOLUTION_DIR") || !data["SOLUTION_DIR"].is_string())
        throw std::runtime_error("CONFIG_MISSING_SOLUTION_DIR");
    if (!data.contains("CODE_TEMPLATE_DIR") || !data["CODE_TEMPLATE_DIR"].is_string())
        throw std::runtime_error("CONFIG_MISSING_CODE_TEMPLATE_DIR");

    AppConfig config;
    config.solutions_dir = data["SOLUTION_DIR"].get<std::string>();
    config.templates_dir = data["CODE_TEMPLATE_DIR"].get<std::string>();
    config.open_cmd = data.value("OPEN_IN_IDE_CMD", "xdg-open");
    return config;
}

std::vector<std::string> list_solutions(const AppConfig& config) {
    return list_entries(config.solutions_dir, true);
}

std::vector<std::string> list_templates(const AppConfig& config) {
    return list_entries(config.templates_dir, false);
}

std::string solution_description(const AppConfig& config, const std::string& name) {
    return read_description(config.solutions_dir / name / "config.json", "Description", "Solution config not found");
}

std::string template_description(const AppConfig& config, const std::string& name) {
    return read_description(config.templates_dir / name, "description", "Template not found");
}

void create_solution(const AppConfig& config, const std::string& name, const std::string& template_name) {
    validate_name(name);

    json tmpl = read_json(config.templates_dir / template_name,
                          "ERROR_TEMPLATE_NOT_FOUND",
                          "ERROR_TEMPLATE_PARSE_ERROR");

    fs::path dir = config.solutions_dir / name;
    fs::path src = dir / "_src_";

    if (fs::exists(src))
        throw std::runtime_error("ERROR_SOLUTION_ALREADY_EXISTS");

    fs::create_directories(src);

    if (tmpl.contains("TREE"))
        build_tree(tmpl["TREE"], src);

    if (tmpl.contains("FILES")) {
        for (const auto& entry : tmpl["FILES"]) {
            fs::path target = safe_path(src, entry.at("name").get<std::string>());
            if (!fs::exists(target))
                throw std::runtime_error("ERROR_FILE_NOT_IN_TREE");

            std::ofstream file(target);
            file << entry.value("ctx", "");
        }
    }

    json solution_config;
    for (const auto& [key, value] : tmpl.items()) {
        if (key != "TREE" && key != "FILES")
            solution_config[key] = value;
    }

    std::ofstream file(dir / "config.json");
    file << solution_config.dump(4);
}

void open_solution(const AppConfig& config, const std::string& name) {
    fs::path src = solution_dir(config, name) / "_src_";

    std::cout << echo("Opening solution in IDE...") << '\n';
    std::system((config.open_cmd + " " + src.string()).c_str());
}

void delete_solution(const AppConfig& config, const std::string& name) {
    fs::remove_all(solution_dir(config, name));
}
