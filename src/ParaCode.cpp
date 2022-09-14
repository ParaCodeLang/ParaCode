#include "ParaCode.h"

#include "repl/repl.h"

#include <boost/filesystem.hpp>

BasicValue* ParaCode::eval(std::string data, std::string filename, bool interpret, std::list<std::string> defaultImports, SourceLocation* sourceLocation) {
    this->initialized = true;
    std::string debugName = "<none>";

    if (filename != "") {
        if (!boost::filesystem::exists(filename)) {
            std::cout << "Script '" << filename << "' could not be found" << std::endl;
            return nullptr;
        }
        this->file = open(filename, 'r');
        debugName = filename;
        this->data = this->file.read();
    }
    else if (data != "") {
        this->data = data;
    }
    else {
        this->data = "";
    }

    //
    return nullptr;
}

BasicValue* ParaCode::evalFile(std::string filename) {
    return eval(nullptr, filename);
}

BasicValue* ParaCode::evalData(std::string data) {
    return eval(data);
}

void ParaCode::repl() {
    Repl repl = Repl(this);
    repl.loop();
}
