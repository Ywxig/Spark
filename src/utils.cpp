#include "../include/utils.h"

// --- split ---
vector<string> split(const string& s, const string& delimiter) {
    vector<string> tokens;
    size_t start = 0;
    size_t end = s.find(delimiter);

    while (end != string::npos) {
        tokens.push_back(s.substr(start, end - start));
        start = end + delimiter.length();
        end = s.find(delimiter, start);
    }
    tokens.push_back(s.substr(start));
    return tokens;
}

// --- join ---
string join(vector<string> vec, string sep) {
    ostringstream oss;
    if (!vec.empty()) {
        copy(vec.begin(), vec.end() - 1, ostream_iterator<string>(oss, sep.c_str()));
        oss << vec.back();
    }
    return oss.str();
}

// --- file class ---
void file::nwf(string file_for_input, string string_for_input) {
	// create new file with content
    ofstream out(file_for_input);
    out << string_for_input;
    out.close();
}

void file::addctx(string file_for_input, string string_for_input) {
	// add content to existing file
    ofstream out(file_for_input, ios::app);
    out << string_for_input;
    out.close();
}

string file::rdf(string file_to_read) {
	// read content from file
    string line;
    vector<string> return_string;

    ifstream in(file_to_read);
    if (in.is_open()) {
        while (getline(in, line))
            return_string.push_back(line);
    } else {
        return_string.push_back("");
    }
    in.close();

    ostringstream oss;
    string sep = " ";
    if (!return_string.empty()) {
        copy(return_string.begin(), return_string.end() - 1, ostream_iterator<string>(oss, sep.c_str()));
        oss << return_string.back();
    }
    return oss.str();
}

// --- utility functions ---
void newFile(string file_for_input, string string_for_input) {
    ofstream out(file_for_input);
    out << string_for_input;
    out.close();
}

vector<string> SplitOnFild(string content) {
    return split(content, "<cut>");
}

string int_to_str(int num) {
    ostringstream ost;
    ost << num;
    return ost.str();
}

void printv(vector<string> arr) {
    for (const auto& elem : arr)
        cout << elem;
}