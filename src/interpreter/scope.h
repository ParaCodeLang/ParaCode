#pragma once

#include <iterator>
#include <algorithm>

class SymbolInfo {
public:
    std::string varname;
    void* declltype;
    BasicValue* valueWrapper;
    bool allowCasting;

    SymbolInfo() = default;
    SymbolInfo(std::string varname, void* declltype, bool value = false, bool allowCasting = false) {
        this->varname = varname;
        this->declltype = declltype;
        this->valueWrapper = new BasicValue(&value);
        this->allowCasting = allowCasting;
    }
};

class Scope
{
public:
    std::map<std::string, SymbolInfo> variables;
    Scope* parent;

    Scope() = default;

    Scope(Scope* parent = nullptr) {
        this->variables = {};
        this->parent = parent;
    }

    BasicValue* declare_variable(std::string name, void* declltype, bool allowCasting = false) {
        this->variables[name] = SymbolInfo(name, declltype, allowCasting);

        return this->variables[name].valueWrapper;
    }

    std::string toString() const {
        std::string result = "Scope definitions: {";
        for (auto it = this->variables.begin(); it != this->variables.end(); ++it) {
            result += it->first;
            result += ": ";
            result += Util::toString(it->second);
            if (it != this->variables.end())
                result += ", ";
        }
        result += "}";
        return result;
    }
};
