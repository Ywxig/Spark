#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <direct.h>
#include <cstdio>
#include <vector>

using namespace std;

class Template {
    public:
    vector<string> laodTemplate(string template_path) {
        // this method load a temlate as vector of string
        // all lise seporeted by "\n" are stored as elements of vector 
        vector<string> template_lines;
        template_lines = m_split(m_rdf(template_path), "\n");
        return template_lines;
    }

    private:
    vector<string> m_split(const string& s, const string& delimiter) {
    vector<string> tokens;
    size_t start = 0;
    size_t end = s.find(delimiter); // Find first occurrence of delimiter

    while (end != string::npos) {
        tokens.push_back(s.substr(start, end - start)); // Extract substring
        start = end + delimiter.length(); // Move start past the delimiter
        end = s.find(delimiter, start); // Find next occurrence
    }
    tokens.push_back(s.substr(start)); // Add the last token
    return tokens;
}
    private:
	string m_join(std::vector<string> vec, string sep = " ") {// ôóíêöèÿ ñîåäèíåíèÿ âñåõ ýëåìåíòîâ âåêòîðà â îäíó ñòðîêó ñ ðàçäåëèòåëåì
	
		std::ostringstream oss;
		if (!vec.empty()) {
			std::copy(vec.begin(), vec.end() - 1, ostream_iterator<string>(oss, sep.c_str()));
			oss << vec.back();
		}
		return oss.str();
	}

        private:
        string m_rdf(string file_to_read) {
	    	std::string line;
	    	vector<string> return_string;
                
	    	std::ifstream in(file_to_read); // îêðûâàåì ôàéë äëÿ ÷òåíèÿ
	    	if (in.is_open())
	    	{
	    		while (getline(in, line))
	    		{
	    			return_string.push_back( line );
	    		}
	    	}
	    	else {
	    		return_string.push_back( "" );
	    	}
	    	in.close();     // çàêðûâàåì ôàéë
	    	return m_join(return_string);
	    }

};