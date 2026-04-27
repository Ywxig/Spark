#include <iostream>
#include <iomanip>

void colorize(const std::string& text, const std::string& color) {
    std::cout << "\033[" << color << "m" << text << "\033[0m" << std::endl;
}



int main() {
    int v1, v2;
    std::cin >> v1 >> v2;
    
    if (v1 > v2) {
        int count = static_cast<int>(v1 / v2);
        colorize("в большую цистерну (1) поместится " + std::to_string(count) + " полных малых (2).", "32"); // green color
    } else {
        int count = static_cast<int>(v2 / v1);
        colorize("в большую цистерну (2) поместится " + std::to_string(count) + " полных малых (1).", "31"); // red color
    }
    
    return 0;
}