#pragma once

#include "util.h"

#include <boost/any.hpp>

class Scope;
class BasicType;

class BasicValue {
public:
    boost::any value;
    
    BasicValue(boost::any value) {
        this->assignValue(value);
    }

    virtual bool compareValue(BasicValue* other) {
        return Util::anyEquals(this->extractValue(), other->extractValue());
    }

    void assignValue(boost::any value) {
        this->value = value;
    }

    virtual BasicValue* extractBasicValue() {
        if (!this->value.empty() && Util::isType<BasicValue>(this->value))
            return boost::any_cast<BasicValue*>(this->value)->extractBasicValue();

        return this;
    }

    virtual boost::any extractValue() {
        if (Util::isType<BasicValue>(this->value))
            return boost::any_cast<BasicValue*>(this->value)->extractValue();

        return this->value;
    }

    virtual BasicValue* lookupType(Scope* globalScope);

    virtual BasicValue* clone() {
        return new BasicValue(this->value);
    }

    virtual std::string toString() const {
        std::string result = Util::toString(this->value);
        return result;
    }
};
