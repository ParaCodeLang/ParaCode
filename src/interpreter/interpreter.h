#pragma once

#include "util.h"
#include "scope.h"
#include "parse/source_location.h"
#include "error.h"
#include "lexer.h"

#include <stdexcept>

class ReturnJump : public std::runtime_error
{
public:
    virtual const char* what() const noexcept {
        return "ReturnJump";
    }
};

class Interpreter
{
public:
    SourceLocation* sourceLocation;
    ErrorList* errorList;
    //Stack* stack;
    
    bool inTry;
    
    Scope* globalScope;

    Interpreter() = default;
    Interpreter(SourceLocation* sourceLocation) {
        this->sourceLocation = sourceLocation;
        this->errorList = new ErrorList();
        // declare scopes + global scope
        //this->stack = new Stack();

        this->inTry = false;

        this->globalScope = new Scope(nullptr);
        // this->m_TopLevelScope = nullptr;
    }
};
