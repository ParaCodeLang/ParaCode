#include "basic_value.h"

#include "parse/node.h"
#include "interpreter/typing/basic_type.h"
#include "interpreter/function.h"
#include "interpreter/scope.h"

namespace Util {
    template<> std::string toString(const BasicValue& t) { return t.toString(); }
}

BasicValue* BasicValue::lookupType(Scope* globalScope) {
    if (Util::isType<BasicValue>(this->value)) {
        return boost::any_cast<BasicValue*>(this->value)->lookupType(globalScope);
    }
    else if (Util::isType<NodeFunctionExpression>(this->value) || Util::isType<ParaCodeLanguage::BuiltinFunction>(this->value)) {
        return globalScope->findVariableValue("Func");
    }
    else if (Util::isType<NodeMacro>(this->value)) {
        return globalScope->findVariableValue("Macro");
    }
    else if (Util::isType<std::string>(this->value)) {
        return globalScope->findVariableValue("Str");
    }
    else if (Util::isType<int>(this->value)) {
        return globalScope->findVariableValue("Int");
    }
    else if (Util::isType<float>(this->value)) {
        return globalScope->findVariableValue("Float");
    }
    else if (Util::isVector(this->value)) {
        return globalScope->findVariableValue("Array");
    }
    else if (Util::isMap(this->value)) {
        return globalScope->findVariableValue("Dict");
    }
    else if (Util::isType<bool>(this->value)) {
        return globalScope->findVariableValue("Bool");
    }
    else if (this->value.empty()) {
        return globalScope->findVariableValue("Null");
    }
    else {
        throw std::runtime_error(Util::format("could not get type for %s", Util::toString(*this)));
    }
}
