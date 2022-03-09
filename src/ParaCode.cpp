#include "ParaCode.h"

#include "repl/repl.h"

BasicValue* ParaCode::eval(std::string data, std::string filename, bool interpret, std::list<std::string> defaultImports, SourceLocation* sourceLocation) {
    return nullptr;
}

BasicValue* ParaCode::evalFile(std::string filename) {
    return eval(filename);
}

BasicValue* ParaCode::evalData(std::string data) {
    return eval(data);
}

void ParaCode::repl() {
    Repl repl = Repl(this);
    repl.loop();
}
