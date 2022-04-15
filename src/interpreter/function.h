#pragma once

#include "interpreter/typing/basic_type.h"
#include "parse/node.h"

#include <boost/any.hpp>

class Interpreter;

namespace ParaCodeLanguage {
    class Function {
    public:
        std::string name;
        boost::any returnType;
        AstNode* node;
        
        Function(std::string name, boost::any returnType, AstNode* node) {
            this->name = name;
            this->returnType = returnType;
            this->node = node;
        }

        inline bool operator==(const Function& rhs) { return this->name == rhs.name; }
        inline bool operator!=(const Function& rhs) { return !(*this == rhs); }

        std::string toString() const {
            return "Function";
        }
    };

    class BuiltinFunctionArguments : public Function {
    public:
        Interpreter* interpreter;
        BasicType* thisObject;
        std::vector<BasicValue*> arguments;
        AstNode* node;
        
        BuiltinFunctionArguments(Interpreter* interpreter, BasicType* thisObject, std::vector<BasicValue*> arguments, AstNode* node) : Function("", boost::any(), node) {
            this->interpreter = interpreter;
            this->thisObject = thisObject;
            this->arguments = arguments;
            this->node = node;
        }
    };

    class BuiltinFunction : public Function {
    public:
        std::function<BasicValue*(BuiltinFunctionArguments)> callback;
        
        BuiltinFunction(std::string name, boost::any returnType, std::function<BasicValue*(BuiltinFunctionArguments)> callback) : Function(name, returnType, nullptr) {
            this->callback = callback;
        }

        BasicValue* call(boost::any args) {
            if (!Util::isType<BuiltinFunctionArguments>(args)) {
                throw std::runtime_error("BuiltinFunction.call expects args as BuiltinFunctionArguments");
            }
            return this->callback(boost::any_cast<BuiltinFunctionArguments>(args));
        }

        bool compareValue(BuiltinFunction other) {
            return *this == other;
        }

        std::string toString() const {
            return Util::format("BuiltinFunction[%s]", this->name.c_str());
        }
    };
}
