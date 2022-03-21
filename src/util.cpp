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

    // trim from start (in place)
    void ltrim(std::string &s) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
            return !std::isspace(ch);
        }));
    }

    // trim from end (in place)
    void rtrim(std::string &s) {
        s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), s.end());
    }

    // trim from both ends (in place)
    void trim(std::string &s) {
        ltrim(s);
        rtrim(s);
    }

    // trim from start (copying)
    std::string ltrimCopy(std::string s) {
        ltrim(s);
        return s;
    }

    // trim from end (copying)
    std::string rtrimCopy(std::string s) {
        rtrim(s);
        return s;
    }

    // trim from both ends (copying)
    std::string trimCopy(std::string s) {
        trim(s);
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
}