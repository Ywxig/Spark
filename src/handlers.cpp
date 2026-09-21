#include <iostream>
#include <string>
#include "handlers.hpp"
#include "solutions.hpp"
#include "../includes/colorise.hpp"

void handler_create(const std::string& solution_name, const std::string& tmpl_name) {
    try {
        Solution solution(solution_name);
        solution.create();
        solution.loadTemplate(tmpl_name);
        solution.build();
    } catch (const std::exception& e) {
        std::cout << echo(e.what());

    }
}

void handler_open(const std::string& solution_name) {
    std::cout << echo("Opening " + solution_name + " in IDE... handlers.cpp");
    try {
        Solution solution(solution_name);
        solution.open_in_ide();
    } catch (const std::exception& e) {
        std::cout << echo(e.what());
    }
}

void handler_solution_index() {
    try {
        for (const auto& solution_name : Solution::index_sons()) {
            std::cout << solution_name << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << echo(e.what());
    }
}

void handler_template_index() {
    try {
        for (const auto& tmpl_name : Solution::index_tmpl()) {
            std::cout << tmpl_name << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << echo(e.what());
    }
}

void handler_delete(const std::string& solution_name) {
    try {
        Solution::delete_solution(solution_name);
    } catch (const std::exception& e) {
        std::cout << echo(e.what());
    }
}
