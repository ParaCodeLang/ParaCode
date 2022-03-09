#pragma once

#include "util.h"

#include "interpreter/basic_value.h"
#include "parse/source_location.h"

class ParaCode
{
public:
    std::string data = "";
    bool initialized = false;

    // Language Info
    std::string version = "2.1.0";
    std::string releaseStage = "development";

    ParaCode() = default;

    BasicValue* eval(std::string data = "", std::string filename = "", bool interpret = true, std::list<std::string> defaultImports={ "std/__core__.para" }, SourceLocation* sourceLocation = nullptr);
    BasicValue* evalFile(std::string filename);
    BasicValue* evalData(std::string data);

    // void callFunction(functionName, arguments=[]) {
    //     // if (!this->initialized)
    //     //   this->eval()
    //     if (this->interpreter == nullptr)
    //         raise Exception("ParaCode not initialized! please run ")
    //     if (type(arguments) != list)
    //         raise Exception("Arguments type is not list!")

    //     return this->interpreter.callFunction(functionName, arguments)
    // }

    void repl();
};
