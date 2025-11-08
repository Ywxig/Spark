/*
main.cpp - main source file for CLI scaffolding tool, like VS template.
This file contains the entry point of the application.

├─ /src
│  ├─ main.cpp                ← точка входа
│  ├─ cli.cpp                 ← обработка аргументов командной строки
│  ├─ scaffolder.cpp          ← логика создания проекта
│  ├─ file_utils.cpp          ← операции с файлами/папками
│  ├─ template_manager.cpp    ← работа с шаблонами
│  └─ config.cpp              ← загрузка config.json

*/

#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <direct.h> // For _getcwd
#include <windows.h> // For Windows-specific functions
#include "cli.cpp" // Include the CLI handling code

// ANSI escape codes for text colors
#define RESET "\033[0m"
#define BLACK "\033[30m"
#define RED "\033[31m"
#define GREEN "\033[32m"
#define YELLOW "\033[33m"
#define BLUE "\033[34m"
#define MAGENTA "\033[35m"
#define CYAN "\033[36m"
#define WHITE "\033[37m"

// ANSI escape codes for background colors
#define BG_BLACK "\033[40m"
#define BG_RED "\033[41m"
#define BG_GREEN "\033[42m"
#define BG_YELLOW "\033[43m"
#define BG_BLUE "\033[44m"
#define BG_MAGENTA "\033[45m"
#define BG_CYAN "\033[46m"
#define BG_WHITE "\033[47m"

using namespace std;

int main() {

    system("title Spark 1.0");

    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode;

    // Get the current console mode
    GetConsoleMode(hConsole, &dwMode);

    // Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hConsole, dwMode);

    cout << "Wellcome in scafolding tool Spark" << endl;
    cout << "Your projects :" << endl;
        handle_commands hc;
        hc.ls_files("."); // list all projects in solutions/
    cout << endl;
    
    for (;;) { // main loop
        cout << RESET;
        try {
            exec();
        } catch (const std::runtime_error& e) {
            cout << RED << "[ERR:] "<< RESET << e.what() << RESET << endl;
        }
        
    }
    return 0;

}