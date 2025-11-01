#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <map>
#include "utils.cpp"
#include <functional>

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

string buffer = "E:\\c++\\snake-platform";

bool scrape_command() {

    string command = "help";
    cout << " >" << CYAN <<" $: " << YELLOW;
    getline(cin, command);

    vector<string> parts = split(command, " ");

    if (parts.size() == 0) {
        cout << "No command entered." << endl;
        return false;
    }

    string cmd = parts[0];

    // Define command handlers using a map
    map<string, function<bool(vector<string>&)>> command_map;
    command_map.emplace("help", [](vector<string>& args) {
        cout << RESET << "Available commands:" << YELLOW << "help, exit, echo" << RESET << endl;
        return true;
    });
    command_map.emplace("exit", [](vector<string>& args) {
        cout << RESET << "Exiting program." << endl;
        exit(0);
        return true;
    });
    command_map.emplace("echo", [](vector<string>& args) {
        string OUTPUT = join(args);
        cout << RESET << OUTPUT << endl;
        return true;
    });
    command_map.emplace("cls", [](vector<string>& args){
        #ifdef _WIN32
            system("cls");
        #else
            system("clear");
        #endif
        return true;
    });
    command_map.emplace("new", [](vector<string>& args){
        string name_new_project = buffer + "\\" + args[1];
        string agres_for_new_project = args.size() > 2 ? args[2] : "";
        string type_of_project = args.size() > 3 ? args[3] : "";
        cout << buffer << endl;

        // make directory and files
        if (!name_new_project.empty()) {
            
            _mkdir(name_new_project.c_str());
            cout << name_new_project << " project created successfully." << endl;
            WriteInFile(name_new_project, "// Snake main file\n");
            return true;
        } else {
            cout << "No project name specified." << endl;
            return false;
        }
    });

    // Remove the command part for argument passing
    parts.erase(parts.begin());

    auto it = command_map.find(cmd);
    if (it != command_map.end()) {
        return it->second(parts);
    } else {
        cout << "Unknown command: " << cmd << endl;
        return false;
    }
}