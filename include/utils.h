#pragma once
#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <vector>
#include <string>

using namespace std;

// --- split ---
vector<string> split(const string& s, const string& delimiter);

// --- join ---
string join(vector<string> vec, string sep = " ");

// --- file class ---
class file {
public:
    void nwf(string file_for_input, string string_for_input);
    void addctx(string file_for_input, string string_for_input);
    string rdf(string file_to_read);
};

// --- utility functions ---
void newFile(string file_for_input, string string_for_input);
vector<string> SplitOnFild(string content);
string int_to_str(int num);
void printv(vector<string> arr);