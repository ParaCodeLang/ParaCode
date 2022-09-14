#pragma once

#include "interpreter/basic_value.h"

#include <math.h>

BasicValue* builtinIntAdd(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs + rhs);
}

BasicValue* builtinIntSub(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs - rhs);
}
    
BasicValue* builtinIntMul(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs * rhs);
}

BasicValue* builtinIntExpon(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) pow(lhs, rhs));
}

BasicValue* builtinIntDiv(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs / rhs);
}

BasicValue* builtinIntBitor(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs | rhs);
}

BasicValue* builtinIntBitand(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs & rhs);
}

BasicValue* builtinIntBitxor(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs ^ rhs);
}

BasicValue* builtinIntMod(BuiltinFunctionArguments arguments) {
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs % rhs);
}

BasicValue* builtinIntBitshiftleft(BuiltinFunctionArguments arguments) {
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs << rhs);
}

BasicValue* builtinIntBitshiftright(BuiltinFunctionArguments arguments) {
    int lhs = boost::any_cast<int>(arguments.arguments[0].extractValue());
    int rhs = boost::any_cast<int>(arguments.arguments[1].extractValue());
    
    return new BasicValue((int) lhs >> rhs);
}

BasicValue* builtinFloatAdd(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs + rhs);
}

BasicValue* builtinFloatSub(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs - rhs);
}
    
BasicValue* builtinFloatMul(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs * rhs);
}

BasicValue* builtinFloatExpon(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) pow(lhs, rhs));
}

BasicValue* builtinFloatDiv(BuiltinFunctionArguments arguments) {
    Interpreter* interpreter = arguments.interpreter;
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs / rhs);
}
    
BasicValue* builtinFloatMod(BuiltinFunctionArguments arguments) {
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs % rhs);
}

BasicValue* builtinFloatBitshiftleft(BuiltinFunctionArguments arguments) {
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs << rhs);
}

BasicValue* builtinFloatBitshiftright(BuiltinFunctionArguments arguments) {
    float lhs = boost::any_cast<float>(arguments.arguments[0].extractValue());
    float rhs = boost::any_cast<float>(arguments.arguments[1].extractValue());
    
    return new BasicValue((float) lhs >> rhs);
}
