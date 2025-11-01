// this file is storege of commands for cli tool

#include <iostream>
#include <filesystem> // For std::filesystem
#include <direct.h>

using namespace std;

// Function to execute commands
void new_project(
    string name_new_project,    // name of new project
    string language,            // programming language
    string type_of_project      // type of project
    ) 
    {

    // make directory and files
    if (!name_new_project.empty()) {
        _mkdir(name_new_project.c_str());
    }
}