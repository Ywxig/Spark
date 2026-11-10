#include <exception>
#include <iostream>
#include <string>
#include <fstream>

#include "src/includes/colorise.hpp"
#include "src/includes/solutions.hpp"

// spark open <target>            - открыть решение
// spark ls [t]                   - показать решения или шаблоны
// spark create <name> <template> - создать решение
// spark del <name>               - удалить решение

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << echo(
            "Usage: " + std::string(argv[0]) + " <option> [args...]\n"
            "Options:\n"
            " <yellow> open <reset> <target>             Open a solution\n"
            " <yellow> ls <reset> [t]                    List solutions or templates\n"
            " <yellow> create <reset> <name> <template>  Create a solution\n"
            " <yellow> del <reset> <name>                Delete a solution") << '\n';
        return 1;
    }

    const std::string option = argv[1];

    // инициализация
    // пока что просто добавления аляса по адресу второго аргумента
    if (option == "init") {
            std::cout << "init spark to: " << (argc > 2 ? argv[2] : "default") << std::endl;

            // Пример добавления алиаса в файл (например, в example.txt или ваш конфиг оболочки)
            std::ofstream file(argv[2], std::ios::app);

            // Вызываем функцию executable_dir() из пространства имен Config и переводим в string
            std::cout << Config::executable_dir().string() << std::endl;

            if (file.is_open()) {
                // Исправлено экранирование кавычек для алиаса
                file << "alias spark=\"" << Config::executable_dir().string() << "/main\"\n";
                file.close();
                std::cout << "SUCCES!" << std::endl;
            } else {
                std::cerr << "Err!!!." << std::endl;
            }
        }

    if (option != "open" && option != "ls" && option != "create" && option != "del") {
        std::cout << "Unknown option: " << option << '\n';
        return 1;
    }

    try {
        const AppConfig config = load_app_config();

        if (option == "open") {
            if (argc < 3) {
                std::cout << "Error: open requires a solution name.\n";
                for (const auto& name : list_solutions(config))
                    std::cout << echo(" <cyan> " + name + " <reset> - " + solution_description(config, name)) << '\n';
                return 1;
            }

            open_solution(config, argv[2]);
        } else if (option == "ls") {
            if (argc >= 3 && std::string(argv[2]) == "t") {
                for (const auto& name : list_templates(config))
                    std::cout << echo(" <cyan> " + name + " <reset> - " + template_description(config, name)) << '\n';
            } else {
                for (const auto& name : list_solutions(config))
                    std::cout << echo(" <cyan> " + name + " <reset> - " + solution_description(config, name)) << '\n';
            }
        } else if (option == "create") {
            if (argc < 4) {
                std::cout << "Error: create requires <solution_name> and <template_name>.\n";
                for (const auto& name : list_templates(config))
                    std::cout << echo(" <cyan> " + name + " <reset> - " + template_description(config, name)) << '\n';
                return 1;
            }

            std::cout << echo("Creating solution " + std::string(argv[2]) +
                              " from template " + argv[3] + "...") << '\n';
            create_solution(config, argv[2], argv[3]);
        } else if (option == "del") {
            if (argc < 3) {
                std::cout << "Error: delete requires a solution name.\n";
                return 1;
            }

            std::cout << "Are you sure you want to delete " << argv[2] << "? (y/N)\n";

            char confirm = 'n';
            std::cin >> confirm;
            if (confirm == 'y' || confirm == 'Y')
                delete_solution(config, argv[2]);
        }
    } catch (const std::exception& error) {
        std::cout << echo(error.what()) << '\n';
        return 1;
    }

    return 0;
}
