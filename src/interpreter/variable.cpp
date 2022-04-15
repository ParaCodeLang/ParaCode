#include "variable.h"

VariableType VariableType::Auto = VariableType("Auto", "auto");
VariableType VariableType::Int = VariableType("Int", "int");
VariableType VariableType::String = VariableType("String", "str");
VariableType VariableType::Any = VariableType("Any", "any");
VariableType VariableType::Function = VariableType("Function", "func");
VariableType VariableType::Type = VariableType("Type", "type");

VariableType VariableType::Array = VariableType("Array", 1);
VariableType VariableType::Dict = VariableType("Dict", 2);
VariableType VariableType::Object = VariableType("Object", 3);

std::map<std::string, VariableType> VariableType::s_Values = {
    { VariableType::Auto.name, VariableType::Auto },
    { VariableType::Int.name, VariableType::Int },
    { VariableType::String.name, VariableType::String },
    { VariableType::Any.name, VariableType::Any },
    { VariableType::Function.name, VariableType::Function },
    { VariableType::Type.name, VariableType::Type },

    { VariableType::Array.name, VariableType::Array },
    { VariableType::Dict.name, VariableType::Dict },
    { VariableType::Object.name, VariableType::Object }
};
