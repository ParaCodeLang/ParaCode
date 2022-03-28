#pragma once

#include "util.h"

class Scope;

class BasicValue
{
public:
    void* value;
    
    BasicValue(void* value) {
        this->assignValue(value);
    }

    bool compareValue(BasicValue* other) {
        return this->extractValue() == other->extractValue();
    }

    void assignValue(void* value) {
        this->value = value;
    }

    BasicValue* extractBasicValue() {
        if (this->value != nullptr && Util::isType<BasicValue>(this->value))
            return ((BasicValue*) this->value)->extractBasicValue();

        return this;
    }

    void* extractValue() {
        if (Util::isType<BasicValue>(this->value))
            return ((BasicValue*) this->value)->extractValue();

        return this->value;
    }

    void* lookupType(Scope* globalScope) {
        return nullptr;
    }

    BasicValue* clone() {
        return new BasicValue(this->value);
    }

    std::string toString() const {
        std::string result = Util::toString(this->value);
        return result;
    }
};
