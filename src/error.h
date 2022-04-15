#pragma once

#include "util.h"
#include "parse/node.h"

#include <stdexcept>

enum ErrorType {
    Exception = 1,
    Syntax = 2,
    DoesNotExist = 3,
    TypeError = 4,
    MultipleDefinition = 5,
    ArgumentError = 6,
    MacroExpansionError = 7,
    InterruptedError = 8
};

class InterpreterError : public std::runtime_error {
public:
    std::string m;
    AstNode* node;
    ErrorType type;
    std::string message;
    bool cont;
    std::string name;
    std::vector<std::string> classnames;
    boost::any object;
    
    InterpreterError() = default;
    InterpreterError(std::string m, AstNode* node = nullptr, ErrorType type = ErrorType::Exception, std::string message = "", bool cont = false, std::string name = "", std::vector<std::string> classnames = {}, boost::any object = boost::any()) : std::runtime_error(m) {
        this->m = m;
        this->node = node;
        this->type = type;
        this->message = message;
        this->cont = cont;
        this->name = name;
        this->classnames = classnames;
        this->object = object;
    }

    virtual const char* what() const noexcept {
        return m.c_str();
    }
};

class Error {
public:
    ErrorType type;
    std::string filename;
    std::string message;
    std::tuple<int, int> location;
    std::string name = "Exception";

    Error() = default;
    Error(ErrorType type, std::tuple<int, int> location, std::string message, std::string filename, std::string name = "Exception") {
        this->type = type;
        this->filename = filename;
        this->message = message;
        this->location = location;
        this->name = name;
    }

    std::string getFilename() {
        if (this->filename == "") {
            return "<none>";
        }

        return this->filename;
    }

    int getRow() {
        return std::get<1>(this->location);
    }

    int getColumn() {
        return std::get<0>(this->location);
    }

    std::string toString() {
        std::string nstr = this->getFilename() + ":" + Util::toString(this->getRow()) + ":" + Util::toString(this->getColumn()) + ":" + LogColor::Error + this->name + ":" + LogColor::Default;
        return LogColor::Bold + nstr + LogColor::Default + this->message;
    }
};

class ErrorList {
public:
    std::vector<Error> errors;

    ErrorList() = default;

    void clearErrors() {
        this->errors.clear();
    }

    void pushError(Error error) {
        this->errors.push_back(error);
    }

    void printErrors() {
        for (Error error : this->errors) {
            std::cout << Util::toString(error) << std::endl;
        }
    }

    std::vector<Error> getErrors() {
        return this->errors;
    }
};
