#pragma once

#include <boost/any.hpp>
#include <boost/predef.h>
#include <boost/algorithm/string.hpp>

#if BOOST_COMP_GNUC
#include <cxxabi.h>
#endif

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
        if (typeid(K) == typeid(boost::any) && typeid(T) != typeid(boost::any)) {
            return boost::replace_all_copy(std::string(boost::core::demangle(typeid(T).name())), std::string("*"), std::string("")).find(boost::replace_all_copy(std::string(boost::core::demangle(k.type().name())), std::string("*"), std::string(""))) != std::string::npos;
        }
        return std::is_same<typename std::remove_pointer<T>::type, typename std::remove_pointer<typename std::remove_reference<typename std::remove_cv<K>::type>::type>::type>();
    }

    template<typename T, typename K>
    bool isTypeStrict(const K &k) {
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
        stream << t;
        return stream.str();
    }

    template<typename T>
    bool isTuple(const T& t) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::tuple", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::tuple", 0) == 0;
#endif
    }
    template<typename T>
    bool isVector(const T& t) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::vector", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::vector", 0) == 0;
#endif
    }
    template<typename T>
    bool isList(const T& t) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::list", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::list", 0) == 0;
#endif
    }
    template<typename T>
    bool isMap(const T& t) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::map", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::map", 0) == 0;
#endif
    }
    template<typename T, typename K>
    bool isMap(const T& t) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::map", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::map", 0) == 0;
#endif
    }
    template<typename T, typename K>
    bool isMap(const T& t, const K& k) {
#if BOOST_COMP_GNUC
        int status;
        char* demangled = abi::__cxa_demangle(typeid(t).name(), 0, 0, &status);
        bool result = std::string(demangled).rfind("std::map", 0) == 0;
        free(demangled);
        return result;
#else
        return std::string(typeid(t).name()).rfind("std::map", 0) == 0;
#endif
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

    bool anyEquals(const boost::any& lhs, const boost::any& rhs);
}

std::string operator*(const std::string& s, size_t n);
