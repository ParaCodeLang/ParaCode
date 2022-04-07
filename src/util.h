#pragma once

class LogColor {
public:
    static std::string Default;
    static std::string Error;
    static std::string Warning;
    static std::string Info;
    static std::string Bold;
};

namespace Util {
    int versionCompare(std::string v1, std::string v2);

    template<typename T, typename K>
    bool isType(const K &k) {
        return typeid(T).hash_code() == typeid(k).hash_code();
    }

    template<class T>
    std::string toString(const T& t) {
        std::ostringstream stream;
        // const uint8_t* pointer = &t;
        // for (size_t i = 0; i < sizeof(T); ++i)
        // {
        //     stream << "0x" << std::hex << pointer[i];
        // }
        return stream.str();
    }

    std::string replaceAll(const std::string& str, const std::string& toReplace, const std::string& replaceWith);

    template<typename... Args>
    std::string format(const std::string& format, Args... args) {
        int size_s = std::snprintf(nullptr, 0, format.c_str(), args...) + 1; // Extra space for '\0'
        if (size_s <= 0) { throw std::runtime_error("Error during formatting."); }
        auto size = static_cast<size_t>(size_s);
        std::unique_ptr<char[]> buf(new char[size]);
        std::snprintf(buf.get(), size, format.c_str(), args...);
        return std::string(buf.get(), buf.get() + size - 1); // We don't want the '\0' inside
    }

    std::string upper(std::string str);
    std::string lower(std::string str);
    void ltrim(std::string &s);
    void ltrim(std::string &s, std::string &chars);
    void rtrim(std::string &s);
    void rtrim(std::string &s, std::string &chars);
    void trim(std::string &s);
    void trim(std::string &s, std::string &chars);
    std::string ltrimCopy(std::string s);
    std::string ltrimCopy(std::string s, std::string chars);
    std::string rtrimCopy(std::string s);
    std::string rtrimCopy(std::string s, std::string chars);
    std::string trimCopy(std::string s);
    std::string trimCopy(std::string s, std::string chars);
    void ljust(std::string& s, int amount);
    std::string ljustCopy(std::string s, int amount);
    bool isDigits(const std::string &str);
    bool isSpaces(const std::string &str);

    std::string getExtension(const std::string& str);

    std::string readFile(std::string filename);
}
