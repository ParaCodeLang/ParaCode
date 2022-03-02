#pragma once

#include "pch.h"

#include "util.h"

#include "repl/repl.h"
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

    BasicValue* eval(std::string data = "", std::string filename = "", bool interpret = true, std::list<std::string> default_imports={ "std/__core__.para" }, SourceLocation* source_location = nullptr)
    {
        return nullptr;
    }

    BasicValue* eval_file(std::string filename)
    {
        return eval(filename);
    }

    BasicValue* eval_data(std::string data)
    {
        return eval(data);
    }

    // void call_function(function_name, arguments=[])
    // {
    //     // if not self.initialized:
    //     //   self.eval()
    //     if (self.interpreter == nullptr)
    //     {
    //         raise Exception("ParaCode not initialized! please run ")
    //     }
    //     if (type(arguments) != list)
    //     {
    //         raise Exception("Arguments type is not list!")
    //     }

    //     return this.interpreter.call_function(function_name, arguments)
    // }

    void repl()
    {
        Repl repl = Repl(this);
        // repl.loop();
    }
};
