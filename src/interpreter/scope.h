#pragma once

#include <iterator>
#include <algorithm>

class SymbolInfo {
public:
    std::string varname;
    BasicType* declltype;
    BasicValue* valueWrapper;
    bool allowCasting;

    SymbolInfo() = default;
    SymbolInfo(std::string varname, BasicType* declltype, boost::any value = boost::any(), bool allowCasting = false) {
        this->varname = varname;
        this->declltype = declltype;
        this->valueWrapper = new BasicValue(&value);
        this->allowCasting = allowCasting;
    }
};

class Scope
{
public:
    std::map<std::string, SymbolInfo*> variables;
    Scope* parent;

    Scope() = default;

    Scope(Scope* parent = nullptr) {
        this->variables = {};
        this->parent = parent;
    }

    BasicValue* declareVariable(std::string name, BasicType* declltype, bool allowCasting = false) {
        this->variables[name] = new SymbolInfo(name, declltype, boost::any(), allowCasting);

        return this->variables[name]->valueWrapper;
    }

    void setVariable(std::string name, boost::any value) {
        SymbolInfo* var = this->findVariableInfo(name);

        if (var != nullptr) {
            var->valueWrapper->assignValue(value);
        }
    }

    SymbolInfo* findVariableInfo(std::string name, bool limit = false) {
        // if (name != "self") {
        //     std::cout << name << std::endl;
        // }

        if (this->variables.count(name)) {
            return this->variables[name];
        }

        if (limit || this->parent == nullptr) {
            return nullptr;
        }

        try {
            return this->parent->findVariableInfo(name);
        }
        catch (const std::exception&) {
            // TODO: Maybe throw an error.
            return nullptr;
        }
    }

    BasicValue* findVariableValue(std::string name, bool limit = false) {
        return this->findVariableInfo(name, limit)->valueWrapper;
    }

    BasicType* findVariableDecltype(std::string name, bool limit = false) {
        return this->findVariableInfo(name, limit)->declltype;
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

class FunctionScope : public Scope {
    FunctionScope() : Scope(nullptr) {}
};
