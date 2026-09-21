#pragma once

#include <string>

// Обработчики CLI-команд
void handler_create(const std::string& solution_name, const std::string& tmpl_name);
void handler_open(const std::string& solution_name);
void handler_solution_index();
void handler_template_index();
void handler_delete(const std::string& solution_name);
