#pragma once

#include "interpreter/typing/basic_type.h"
#include "interpreter/basic_object.h"
#include "interpreter/variable.h"
#include "interpreter/basic_value.h"
#include "interpreter/function.h"
#include "interpreter/env/builtins.h"

class Globals {
public:
    BasicType* basicType;
    BasicType* basicObject;
    BasicType* funcType;

    Globals() {
        this->basicType = new BasicType(
            nullptr,
            {
                { "name", new BasicValue("Type") },
                { "extend", BuiltinFunction("Type.extend", boost::any(), builtinTypeExtend) },
                // { "type", BuiltinFunction("Type.type", boost::any(), builtinTypeType) },
                // { "is", BuiltinFunction("Type.is", boost::any(), builtinTypeIs) },
                { "to_str", BuiltinFunction("Type.to_str", boost::any(), builtinTypeToStr) },
                // { "new", BuiltinFunction("Object.new", boost::any(), builtinObjectNew) },
            },
            true
        );

        this->basicObject = new BasicType(
            this->basicType,
            {
                { "instance", new BasicObject(nullptr, {}) },
                { "name", new BasicValue("Object") },
                { "new", BuiltinFunction("Object.new", boost::any(), builtinObjectNew) },
                { "type", BuiltinFunction("Object.type", boost::any(), builtinObjectType) },
                { "is", BuiltinFunction("Object.is", boost::any(), builtinObjectIs) },
                { "to_str", BuiltinFunction("Object.to_str", boost::any(), builtinObjectToStr) }
            }
        );

        this->basicType->parent = this->basicObject; // Circular

        this->funcType = new BasicType(
            this->basicType,
            {
                { "name", new BasicValue("Func") },
                { "instance", new BasicObject(nullptr, {}) }
            }
        );
    }

    BasicType* vartypeToTypeobject(VariableType vartype) {
        if (vartype == VariableType::Function) {
            return this->funcType;
        }
        else if (vartype == VariableType::Type) {
            return this->basicType;
        }
        else if (vartype == VariableType::Object) {
            return this->basicObject;
        }

        throw std::runtime_error("No conversion defined for %s", Util::toString(vartype).c_str());
        return nullptr;
    }

    void applyToScope(Scope* scope) {
        for (auto item : this->variables) {
            std::string name = std::get<0>(item);
            VarType vtype = std::get<1>(item);
            boost::any value = std::get<2>(item);
            if (!scope->variables.count(name)) {
                VarType varType = vtype;

                BasicType* typeObject = this->vartypeToTypeobject(varType);

                scope->declareVariable(name, typeObject);

                BasicValue* var = scope->findVariableValue(name);
                var->assignValue(value);
            }
        }
    }
};
