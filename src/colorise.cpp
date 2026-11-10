#include "colorise.hpp"

#include <utility>

namespace {

const std::pair<const char*, const char*> COLORS[] = {
    {"<red>", "\033[31m"},
    {"<green>", "\033[32m"},
    {"<yellow>", "\033[33m"},
    {"<blue>", "\033[34m"},
    {"<magenta>", "\033[35m"},
    {"<cyan>", "\033[36m"},
    {"<white>", "\033[37m"},
    {"<reset>", "\033[0m"},
    {"<enc>", "\033[33m Encrypt: \033[0m"},
    {"<dec>", "\033[33m Decrypt: \033[0m"},
    {"<key>", "\033[33m Key: \033[0m"},
};

void replace_all(std::string& text, const std::string& from, const std::string& to) {
    for (std::size_t pos = 0; (pos = text.find(from, pos)) != std::string::npos; pos += to.size())
        text.replace(pos, from.size(), to);
}

} // namespace

std::string echo(const std::string& message) {
    std::string result = message;
    for (const auto& [tag, code] : COLORS)
        replace_all(result, tag, code);
    return result + "\033[0m";
}
