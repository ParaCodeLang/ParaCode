#pragma once

#include "util.h"

#include "lexer.h"
#include "parse/parser.h"
#include "parse/node.h"
#include "interpreter/basic_value.h"
#include "parse/source_location.h"
#include "interpreter/interpreter.h"
#include "error.h"

class ParaCode {
public:
    std::string data = "";
    bool initialized = false;

    // Language Info
    std::string version = "3.0.0";
    std::string releaseStage = "development";

    ParaCode() = default;

    BasicValue* eval(std::string data = "", std::string filename = "", bool interpret = true, std::list<std::string> defaultImports={ "std/__core__.para" }, SourceLocation* sourceLocation = nullptr);
    BasicValue* evalFile(std::string filename);
    BasicValue* evalData(std::string data);

    void callFunction(functionName, arguments=[]) {
        if (!this->initialized) {
            this->eval();
        }
        if (this->interpreter == nullptr) {
            throw std::runtime_error("ParaCode not initialized! please run ");
        }
        if (!Util::isVector(arguments)) {
            throw std::runtime_error("Arguments type is not vector!");
        }

        return this->interpreter->callFunction(functionName, arguments);
    }

    void repl();
};
