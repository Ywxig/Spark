

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
#include <direct.h> // For _getcwd
#include <cstdio>

using namespace std;

vector<string> split(const string& s, const string& delimiter) {
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

	string join(std::vector<string> vec, string sep = " ") {// ôóíêöèÿ ñîåäèíåíèÿ âñåõ ýëåìåíòîâ âåêòîðà â îäíó ñòðîêó ñ ðàçäåëèòåëåì
	
		std::ostringstream oss;
		if (!vec.empty()) {
			std::copy(vec.begin(), vec.end() - 1, ostream_iterator<string>(oss, sep.c_str()));
			oss << vec.back();
		}
		return oss.str();
	}

    class file{
        public:
	    void nwf(string file_for_input, string string_for_input) {// îáÿâëåíèÿ ìåòîäà WriteInFile
	    	ofstream out(file_for_input);// ñîçäàíèå ïîòîêà äëÿ çàïèñè
	    	out << string_for_input;// çàïèñü ðåçóëüòàòà
	    	out.close();// çàêðûòèå ïîòîêà
	    }

        public:
	    void addctx(string file_for_input, string string_for_input) {// îáÿâëåíèÿ ìåòîäà WriteInFile
	    	ofstream out(file_for_input, std::ios::app);// ñîçäàíèå ïîòîêà äëÿ çàïèñè
	    	out << string_for_input;// çàïèñü ðåçóëüòàòà
	    	out.close();// çàêðûòèå ïîòîêà
	    }

        public:
        string rdf(string file_to_read) {
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
	    	return join(return_string);
	    }
    };

    void newFile(string file_for_input, string string_for_input) {// creating a new file
		ofstream out(file_for_input);// ñîçäàíèå ïîòîêà äëÿ çàïèñè
		out << string_for_input;// çàïèñü ðåçóëüòàòà
		out.close();// çàêðûòèå ïîòîêà
	}

	string Read(string file_to_read) {
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
		return join(return_string);
	}

	vector<string> SplitOnFild(string content) {// ôóíêöèÿ ðàçäåëåíèÿ èñõîäíîãî òåêñòà íà ïîëÿ èëè ðàáî÷èè îáëàñòè
		vector<string> Filds = split(content, "<cut>");// ñàìî ðàçäåëåíèå ïî òåãó <cut>

		return Filds;// âîçâðàùÿåì ìàñèâ ñ ïîëÿìè!
	}

	string int_to_str(int num) {
		std::ostringstream ost;
		ost << num;
		return ost.str();
	}

	
	void printv(vector<string> arr) {
		for (int i = 0; i < arr.size(); i++) {
			cout << arr[i];
		}
	}