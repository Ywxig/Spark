#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <direct.h> // For _getcwd
#include <windows.h> // For Windows-specific functions
#include "command_scraper.cpp"

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

    //vector<string> PATH; // it's for using command lice "cd", "ls" and etc.
    //char buffer[_MAX_PATH];
    //_getcwd(buffer, _MAX_PATH);
    //string BUFFER = ""; 
    //BUFFER = buffer;
    //PATH = split(BUFFER, "\\");

    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode;

    // Get the current console mode
    GetConsoleMode(hConsole, &dwMode);

    // Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hConsole, dwMode);

    cout << "Welcome to snake platform!" << endl;
    
    for (;;) { // main loop
        scrape_command();
    }
    return 0;

}