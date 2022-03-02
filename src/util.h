#pragma once

#include <pch.h>

class LogColor
{
public:
    static std::string Default;
    static std::string Error;
    static std::string Warning;
    static std::string Info;
    static std::string Bold;
};
std::string LogColor::Default = "\033[0m";
std::string LogColor::Error = "\033[31;1m";
std::string LogColor::Warning = "\033[33m";
std::string LogColor::Info = "\033[34m";
std::string LogColor::Bold = "\033[1m";

namespace Util {
    template<typename T, typename K>
    static bool isType(const K &k)
    {
        return typeid(T).hash_code() == typeid(k).hash_code();
    }

    template<class T>
    std::string toString(const T& t)
    {
        std::ostringstream stream;
        // const uint8_t* pointer = &t;
        // for (size_t i = 0; i < sizeof(T); ++i)
        // {
        //     stream << "0x" << std::hex << pointer[i];
        // }
        return stream.str();
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
}
