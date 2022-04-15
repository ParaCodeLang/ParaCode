#pragma once

#include <boost/any.hpp>

class VariableType {
public:
    static std::map<std::string, VariableType> s_Values;

    static VariableType Auto;
    static VariableType Int;
    static VariableType String;
    static VariableType Any;
    static VariableType Function;
    static VariableType Type;

    static VariableType Array;
    static VariableType Dict;
    static VariableType Object; // Class, data structure, etc.

    std::string name;
    boost::any value;

    VariableType() = default;
    VariableType(std::string name, boost::any value) {
        this->name = name;
        this->value = value;
    }

    inline bool operator==(const VariableType& rhs) { return this->name == rhs.name; }
    inline bool operator!=(const VariableType& rhs) { return !(*this == rhs); }
};
