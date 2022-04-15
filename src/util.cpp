#include "util.h"

std::string LogColor::Default = "\033[0m";
std::string LogColor::Error = "\033[31;1m";
std::string LogColor::Warning = "\033[33m";
std::string LogColor::Info = "\033[34m";
std::string LogColor::Bold = "\033[1m";

namespace Util {
    int versionCompare(std::string v1, std::string v2) {
        int vnum1 = 0, vnum2 = 0;

        for (int i = 0, j = 0; (i < v1.length() || j < v2.length());) {
            while (i < v1.length() && v1[i] != '.') {
                vnum1 = vnum1 * 10 + (v1[i] - '0');
                i++;
            }

            while (j < v2.length() && v2[j] != '.') {
                vnum2 = vnum2 * 10 + (v2[j] - '0');
                j++;
            }

            if (vnum1 > vnum2)
                return 1;
            if (vnum2 > vnum1)
                return -1;

            vnum1 = vnum2 = 0;
            i++;
            j++;
        }
        return 0;
    }
    template<> std::string toString(const int& t) { return std::to_string(t); }
    template<> std::string toString(const long& t) { return std::to_string(t); }
    template<> std::string toString(const long long& t) { return std::to_string(t); }
    template<> std::string toString(const unsigned& t) { return std::to_string(t); }
    template<> std::string toString(const unsigned long& t) { return std::to_string(t); }
    template<> std::string toString(const unsigned long long& t) { return std::to_string(t); }
    template<> std::string toString(const float& t) { return std::to_string(t); }
    template<> std::string toString(const double& t) { return std::to_string(t); }
    template<> std::string toString(const std::string& t) { return std::string(t); }

    std::string replaceAll(const std::string& str, const std::string& toReplace, const std::string& replaceWith) {
        return std::regex_replace(str, std::regex(toReplace), replaceWith);
    }

    std::string upper(std::string str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::toupper);
        return result;
    }

    std::string lower(std::string str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }

    // Trim from start (in place)
    void ltrim(std::string &s) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
            return !std::isspace(ch);
        }));
    }
    void ltrim(std::string &s, std::string &chars) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [chars](unsigned char ch) {
            return chars.find(ch) == std::string::npos;
        }));
    }

    // Trim from end (in place)
    void rtrim(std::string &s) {
        s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), s.end());
    }
    void rtrim(std::string &s, std::string &chars) {
        s.erase(std::find_if(s.rbegin(), s.rend(), [chars](unsigned char ch) {
            return chars.find(ch) == std::string::npos;
        }).base(), s.end());
    }

    // Trim from both ends (in place)
    void trim(std::string &s) {
        ltrim(s);
        rtrim(s);
    }
    void trim(std::string &s, std::string &chars) {
        ltrim(s, chars);
        rtrim(s, chars);
    }

    // Trim from start (copying)
    std::string ltrimCopy(std::string s) {
        ltrim(s);
        return s;
    }
    std::string ltrimCopy(std::string s, std::string chars) {
        ltrim(s, chars);
        return s;
    }

    // Trim from end (copying)
    std::string rtrimCopy(std::string s) {
        rtrim(s);
        return s;
    }
    std::string rtrimCopy(std::string s, std::string chars) {
        rtrim(s, chars);
        return s;
    }

    // Trim from both ends (copying)
    std::string trimCopy(std::string s) {
        trim(s);
        return s;
    }
    std::string trimCopy(std::string s, std::string chars) {
        trim(s, chars);
        return s;
    }

    void ljust(std::string& s, int amount) {
        int length = s.length();
        if (length < amount) {
            s += std::string(amount - length, ' ');
        }
    }

    std::string ljustCopy(std::string s, int amount) {
        ljust(s, amount);
        return s;
    }

    bool isDigits(const std::string &str) {
        return std::all_of(str.begin(), str.end(), ::isdigit);
    }

    bool isSpaces(const std::string &str) {
        return std::all_of(str.begin(), str.end(), ::isspace);
    }

    std::string getExtension(const std::string& str) {
        unsigned found = str.find_last_of(".");
        return str.substr(found + 1);
    }

    std::string readFile(std::string filename) {
        std::ifstream t(filename);
        std::stringstream buffer;
        buffer << t.rdbuf();
        return buffer.str();
    }

    bool anyEquals(const boost::any& lhs, const boost::any& rhs) {
        if (lhs.type() != rhs.type()) {
            return false;
        }

        else if (lhs.type() == typeid(std::string)) {
            return boost::any_cast<std::string>(lhs) == boost::any_cast<std::string>(rhs);
        }
        else if (lhs.type() == typeid(int)) {
            return boost::any_cast<int>(lhs) == boost::any_cast<int>(rhs);
        }

        throw std::runtime_error("comparison of any unimplemented for type");
    }
}

std::string operator*(const std::string& s, size_t n) {
    std::string result;
    result.reserve(s.size() * n);
    for (size_t i = 0; i < n; ++i) {
        result += s;
    }
    return result;
}
