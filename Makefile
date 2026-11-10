.PHONY: all run clean deps

CXX      := g++
INCL_DIR := src/includes
CXXFLAGS := -Wall -Wextra -std=c++17

DIST_DIR := dist
TARGET   := $(DIST_DIR)/main
SRCS     := main.cpp $(wildcard src/*.cpp)
HDRS     := $(wildcard $(INCL_DIR)/*.hpp)

JSON_HPP := $(INCL_DIR)/json.hpp

all: deps $(TARGET)
	@mkdir -p $(DIST_DIR)/Templates
	@cp src/config.json $(DIST_DIR)/
	@cp -r Templates/. $(DIST_DIR)/Templates/

deps: | $(INCL_DIR)
	@if [ ! -f $(JSON_HPP) ]; then \
		echo "Скачиваем json.hpp..."; \
		curl -L -o $(JSON_HPP) https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp; \
	fi

$(INCL_DIR):
	mkdir -p $(INCL_DIR)

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

$(TARGET): $(SRCS) $(HDRS) | $(DIST_DIR)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

run: all
	@echo "Building is done"

clean:
	rm -rf $(DIST_DIR)
