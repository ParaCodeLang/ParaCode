#pragma once

#include "util.h"

#include <boost/any.hpp>

class Scope;

class BasicValue {
public:
    boost::any value;
    
    BasicValue(boost::any value) {
        this->assignValue(value);
    }

    bool compareValue(BasicValue* other) {
        return Util::anyEquals(this->extractValue(), other->extractValue());
    }

    void assignValue(boost::any value) {
        this->value = value;
    }

    BasicValue* extractBasicValue() {
        if (!this->value.empty() && Util::isType<BasicValue>(this->value))
            return boost::any_cast<BasicValue*>(this->value)->extractBasicValue();

        return this;
    }

    boost::any extractValue() {
        if (Util::isType<BasicValue>(this->value))
            return boost::any_cast<BasicValue*>(this->value)->extractValue();

        return this->value;
    }

    BasicType* lookupType(Scope* globalScope) {
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
