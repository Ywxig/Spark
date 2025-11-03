#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <cstdlib> // For system()
#include <map>
#include <functional>
#include <filesystem> // For directory iteration

#include "utils.cpp" // Assuming utils.cpp is in the same directory

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

string hovered_project = "~"; // default hovered project

class handle_commands {

public:
void new_project(
    string name_new_project,        // name of new project
    string template_of_project)     // template of new project
    {
        string new_project_path = "solutions/" + name_new_project;
        // make directory and files
        if (!name_new_project.empty()) {
            _mkdir(new_project_path.c_str());
            file f;
            f.nwf(new_project_path + "/README.md", "# " + name_new_project);
        }
    };

public:
void add_file(
    string file_name,               // name of new file
    string content_to_add)          // content to add
    
    {
        vector<string> file_name_vector = split(file_name, "/"); // get only file name from path
        if (file_name_vector[0] == ".") {
        }
        file f;
        f.addctx( "solutions/" + hovered_project + "/" + file_name_vector[1], content_to_add);
    }

public:
void ls_files(string project)            // path to list files
    {
        namespace fs = std::filesystem;
        try {
            if (project == ".") {
                project = "/" + hovered_project;
            } else {
                project = "/" + project;
            } 
            std::string path = "solutions" + project; // путь к папке
            for (const auto& entry : fs::directory_iterator(path)) {
                if (entry.is_directory()) {
                    std::cout << GREEN << entry.path().filename().string() << " " << RESET;
                } else {
                    std::cout << RESET << entry.path().filename().string() << " " << RESET;
                }
            }
        } catch (const std::runtime_error& e) {
            std::string path = "solutions"; // путь к папке
            for (const auto& entry : fs::directory_iterator(path)) {
                if (entry.is_directory()) {
                    std::cout << GREEN << entry.path().filename().string() << " " << RESET;
                } else {
                    std::cout << RESET << entry.path().filename().string() << " " << RESET;
                }
            }   
        }
        cout << endl;
    }
};


void exec() {

    string command = "help";
    cout << GREEN << hovered_project << RESET << " >" << CYAN <<" $: " << YELLOW;
    getline(cin, command);

    vector<string> parts = split(command, " ");

    if (parts.size() == 0) {
        cout << "No command entered." << endl;
        return;
    }

    string cmd = parts[0];

    // Define command handlers using a map
    map<string, function<void(vector<string>&)>> command_map;
    command_map.emplace("help", [](vector<string>& args) {
        cout << RESET << "Available commands:" << YELLOW << "help, exit, echo" << RESET << endl;
        return;
    });

    command_map.emplace("exit", [](vector<string>& args) {
        cout << RESET << "Exiting program." << endl;
        exit(0);
        return;
    });

    command_map.emplace("echo", [](vector<string>& args) {
        string OUTPUT = join(args);
        cout << RESET << OUTPUT << endl;
        return;
    });

    command_map.emplace("cls", [](vector<string>& args){
        #ifdef _WIN32
            system("cls");
        #else
            system("clear");
        #endif
        return;
    });

    command_map.emplace("new", [](vector<string>& args){
        // using exemple: > new new_cli <language> <type_of_project>
        string name_new_project = args[0];
        string template_of_project = args[1];

        // make directory and files
        handle_commands hc;
        hc.new_project(name_new_project, template_of_project);

        // create project structure from template
        //creatProj(name_new_project, template_of_project);
    });

    command_map.emplace("add", [](vector<string>& args){
        // using exemple: > add <file_path> <content_to_add>
        string file_name = args[0];
        string content_to_add = args[1];

        handle_commands hc;
        hc.add_file(file_name, content_to_add);
    });

    command_map.emplace("hover", [](vector<string>& args){
        hovered_project = args[0];
    });

    command_map.emplace("code", [](vector<string>& args){
        if (hovered_project == "~") {
            cout << RESET << "No project hovered. " <<  "Use '" << CYAN <<"hover " << GREEN << "<project_name>" << RESET << "' to hover a project." << endl;
            return;
        }
        system(("code " + hovered_project).c_str());
    });

    command_map.emplace("ls", [](vector<string>& args){
        string project = ".";
        try {
            string project = args[0];
        } catch (const std::out_of_range& e) {
            cout << RESET << "";
        }
        handle_commands hc;
        hc.ls_files(project);
    });

    command_map.emplace("del", [](vector<string>& args){
        string flag = args[1];
        string project = args[0];
        // if project is ".", use hovered_project
        if (project == ".") {project = hovered_project;}

        if (flag == "-r") {
            // remove all files and folders in the project
            // use C++17 filesystem library
            filesystem::remove_all("solutions/" + project);
        } if (flag == "-f") {
            filesystem::remove("solutions/" + project);
        }
    });

    // Remove the command part for argument passing
    parts.erase(parts.begin());

    auto it = command_map.find(cmd);
    if (it != command_map.end()) {
        it->second(parts);
        return;
    } else {
        cout << "Unknown command: " << cmd << endl;
        return;
    }
}