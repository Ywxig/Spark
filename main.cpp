#include <iostream>
#include <string>
#include "handlers.hpp"
#include "includes/colorise.hpp"

// ввод типо spark <opt> ...
// spark open <target> - открыть решение
// spark ls [templates] - показать список решений или шаблонов
// spark create <name> <template> - создать решение
// spark del <name> - удалить решение

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cout << echo(
            "Usage: " + std::string(argv[0]) + " <option> [args...]\n"
            "Options:\n"
            " <yellow> open <reset> <target>             Open a solution\n"
            " <yellow> ls <reset> [templates]            List solutions or templates\n"
            " <yellow> create <reset> <name> <template>  Create a solution\n"
            " <yellow> del <reset> <name>                Delete a solution");
        exit(1);
    }

    std::string opt = argv[1];

    if (opt == "open") {
        if (argc < 3) {
            std::cout << "Error: open requires a solution name." << std::endl;
            return 1;
        }
        handler_open(argv[2]);
    } else if (opt == "ls") {
        if (argc >= 3 && std::string(argv[2]) == "t") {
            handler_template_index();
        } else {
            handler_solution_index();
        }
    } else if (opt == "del") {
        if (argc < 3) {
            std::cout << "Error: delete requires a solution name." << std::endl;
            return 1;
        }
        handler_delete(argv[2]);
    } else if (opt == "create") {
        if (argc < 4) {
            std::cout << "Error: create requires <solution_name> and <template_name>." << std::endl;
            return 1;
        }
        std::string solution_name = argv[2];
        std::string tmpl_name = argv[3];
        std::cout << echo("Creating solution " + solution_name + " from template " + tmpl_name + "...") << std::endl;
        handler_create(solution_name, tmpl_name);
    } else {
        std::cout << "Unknown option: " << opt << std::endl;
        return 1;
    }

    return 0;
}
