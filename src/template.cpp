#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <filesystem>
#include <functional>
#include <fstream>

#include "../include/utils.h" // Your custom file utilities

using namespace std;

class Template {
public:
    void executeTemplate(
        const string& name_new_project,     // name of new project
        const string& template_of_project)  // template file name
    {
        string template_path = "template/" + template_of_project + ".txt";
        file f;
        string template_content = f.rdf(template_path);

        vector<string> lines = split(template_content, "\n");

        // Command registry
        map<string, function<void(vector<string>&)>> template_commands;

        // mkfile
        template_commands.emplace("mkfile", [name_new_project](vector<string>& args) {
            if (args.empty()) {
                cout << "Usage: mkfile <path> <content>\n";
                return;
            }

            file f;
            string path = "solutions/" + name_new_project + "/" + args[0];
            string content = f.rdf("template/code/" + args[1]);

            // Ensure parent directories exist
            filesystem::create_directories(filesystem::path(path).parent_path());

            // Create file and write content
            ofstream out(path);
            if (!out.is_open()) {
                cout << "Error: could not create file '" << path << "'\n";
                return;
            }

            out << content;
            out.close();
        });

        // mkdir
        template_commands.emplace("mkdir", [name_new_project](vector<string>& args) {
            if (args.empty()) {
                cout << "Usage: mkdir <path>\n";
                return;
            }

            string dir_path = "solutions/" + name_new_project + "/" + args[0];
            filesystem::create_directories(dir_path);
        });

        // process each line
        for (const string& line : lines) {
            if (line.empty()) continue;

            vector<string> parts = split(line, " ");
            if (parts.empty()) continue;

            string command = parts[0];
            vector<string> args(parts.begin() + 1, parts.end());

            auto it = template_commands.find(command);
            if (it != template_commands.end()) {
                it->second(args);
            } else {
                cout << "Unknown command: " << command << endl;
            }
        }

        cout << "\n Template applied successfully!\n" << endl;
    }
};