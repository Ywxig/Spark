#include <iostream>
#include <map>
// This module for colorising the output
// We usig ANSI escape codes for colorise text like in colorama
// And we make here a function for positing text in a specific place like center, left, right

// table of color

std::map<std::string, std::string> COLORS = {
    {"red", "\033[31m"},
    {"green", "\033[32m"},
    {"yellow", "\033[33m"},
    {"blue", "\033[34m"},
    {"magenta", "\033[35m"},
    {"cyan", "\033[36m"},
    {"white", "\033[37m"},
    {"reset", "\033[0m"},
};

void print(std::string text, std::string color = "white", bool err_mode = false) {
    // simple fuction for make color in text like red, blue, yellow, green...
    if (!err_mode) {std::cout << COLORS[color] << text << COLORS["reset"];}
    else { std::cerr << COLORS["red"] << "[ERROR] " << COLORS[color] << text << COLORS["reset"]; }   
}