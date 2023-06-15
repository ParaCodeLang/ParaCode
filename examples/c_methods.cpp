// TODO: Rewrite for Rust!!
#include "../src/interpreter/basic_value.h"
#include "../src/interpreter/function.h"
#include "../src/util.h"

BasicValue* p(BuiltinFunctionArguments arguments) {
    if (len(arguments.arguments) > 0) {
        std::cout << Util::toString(arguments.arguments[0]) << std::endl;
        return new BasicValue(arguments.arguments[0].extractValue());
    }
    std::cout << "Nothing provided." << std::endl;
    return new BasicValue("Nothing provided.");
}

// Now just run:
// cimport("examples/c_methods.cpp", {"p": "__p__"});
// to add it to ParaCode.
// The first parameter is the C file's path.
// The second parameter is a dictionary where the keys
// are the C function names and the values are the
// ParaCode function names.
