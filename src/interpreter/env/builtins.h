#pragma once

#include "interpreter/typing/basic_type.h"
#include "interpreter/basic_object.h"
#include "interpreter/variable.h"
#include "interpreter/basic_value.h"
#include "interpreter/function.h"

#include <boost/any.hpp>

std::string objToString(Interpreter* interpreter, AstNode* node, boost::any obj) {
    std::string objStr;
    if (obj.type() == typeid(std::string)) {
        objStr = boost::any_cast<std::string>(obj);
    }
    else if (lhs.type() == typeid(BasicValue)) {
        objStr = Util::toString(boost::any_cast<BasicValue*>(obj));
    }

    obj = interpreter->basicValueToObject(node, obj);

    if (Util::isType<BasicObject>(obj)) {
        meth = boost::any_cast<BasicObject*>(obj)->lookupMember(BasicType::REPR_FUNCTION_NAME);

        basic_value_repr = nullptr;

        if (meth != nullptr):
            if isinstance(meth.value, BuiltinFunction):
                basic_value_repr = interpreter.call_builtin_function(meth.value, obj, [], node)
            else:
                interpreter.stack.push(obj)
                interpreter.call_function_expression(meth.value)
                basic_value_repr = interpreter.stack.pop()

            if not isinstance(basic_value_repr, BasicValue):
                interpreter.error(node, ErrorType.TypeError, 'expected {} method to return an instance of BasicValue, got {}'.format(BasicType.REPR_FUNCTION_NAME, basic_value_repr))
                return None

            objStr = basic_value_repr.value;

    return objStr;
}

void _printObject(Interpreter* interpreter, AstNode* node, boost::any obj, std::string end = "\n") {
    std::cout << objToString(interpreter, node, obj) << end;
}

BasicValue* builtinTypeExtend(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    BasicType* thisObject = arguments.thisObject;

    std::map<std::string, boost::any> extendedProperties = {};
    if (arguments.arguments.size()) > 0) {
        BasicValue* providedArgs = arguments.arguments[0];

        if (!Util::isType<BasicObject>(providedArgs) {
            interpreter->error(Util::format("provided args to Type.extend must be an instance of BasicObject, got %s", Util::toString(providedArgs).c_str()));
            return nullptr;
        }

        extendedProperties = ((BasicObject*) providedArgs)->members;
    }

    std::map<std::string, boost::any> instanceMembers = {};

    if (thisObject->members.count("instance")) {
        instanceMembers = thisObject->members["instance"]->clone()->members;
    }

    instanceMembers.insert(extendedProperties.begin(), extendedProperties.end());

    return new BasicType(thisObject, instanceMembers);
}

BasicValue* builtinTypeToStr(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    BasicValue* thisObject = arguments.thisObject;

    return new BasicValue(Util::toString(thisObject));
}