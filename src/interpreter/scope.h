#pragma once

#include <map>
#include <iterator>
#include <algorithm>

class SymbolInfo
{
public:
    std::string varname;
    void* decltype;
    BasicValue* value_wrapper;
    bool allow_casting;

    SymbolInfo() = default;

    SymbolInfo(std::string varname, void* decltype, bool value = false, bool allow_casting = false)
    {
        this->varname = varname;
        this->decltype = ddecltype
        this->value_wrapper = new BasicValue(value);
        this->allow_casting = allow_casting;
    }
};

class Scope
{
public:
    std::map<std::string, SymbolInfo> variables;
    Scope* parent;

    Scope() = default;

    Scope(Scope* parent = nullptr)
    {
        this->variables = {};
        this->parent = parent;
    }

    BasicValue* declare_variable(std::string name, void* decltype, bool allow_casting = false)
    {
        this->variables[name] = SymbolInfo(name, decltype, allow_casting);

        return this->variables[name].value_wrapper;
    }

    std::string toString() const
    {
        std::string result = "Scope definitions: {";
        // for (std::map<std::string, SymbolInfo>::iterator it = this->variables.begin(); it != this->variables.end(); ++it)
        for (auto const& it : this->variables)
        {
            result += it.first;
            result += ": ";
            result += Util::toString(it->second);
            if (it != this->variables.end())
                result += ", ";
        }
        result += "}";
        return result;
    }
};
