.PHONY: all run clean deps

CXX      := g++
INCL_DIR := includes
# Добавляем -I$(INCL_DIR) — это указывает путь к вашим hpp файлам
CXXFLAGS := -Wall -Wextra -std=c++17 -I$(INCL_DIR)

DIST_DIR := dist
TARGET   := $(DIST_DIR)/main
SRCS     := main.cpp $(wildcard src/*.cpp)

JSON_HPP  := $(INCL_DIR)/json.hpp
CLI11_HPP := $(INCL_DIR)/CLI11.hpp

all: deps $(TARGET) copy_config

deps: | $(INCL_DIR)
	@if [ ! -f $(JSON_HPP) ]; then \
		echo "Скачиваем json.hpp..."; \
		curl -L -o $(JSON_HPP) https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp; \
	fi

$(INCL_DIR):
	mkdir -p $(INCL_DIR)

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

# Сборка проекта
$(TARGET): $(SRCS) | $(DIST_DIR)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

copy_config: config.json | $(DIST_DIR)
	@cp config.json $(DIST_DIR)/
	@cp -r Templates $(DIST_DIR)/

run: all
	@echo "Building is done"

clean:
	rm -rf $(DIST_DIR)
