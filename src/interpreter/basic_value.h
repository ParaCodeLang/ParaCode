#pragma once

#include "util.h"

class Scope;

class BasicValue
{
public:
    void* value;
    
    BasicValue(void* value)
    {
        this->assign_value(value);
    }

    bool compare_value(BasicValue* other)
    {
        return this->extract_value() == other->extract_value();
    }

    void assign_value(void* value)
    {
        this->value = value;
    }

    BasicValue* extract_basicvalue()
    {
        if (this->value != nullptr && Util::isType<BasicValue>(this->value))
            return ((BasicValue*) this->value)->extract_basicvalue();

        return this;
    }

    void* extract_value()
    {
        if (Util::isType<BasicValue>(this->value))
            return ((BasicValue*) this->value)->extract_value();

        return this->value;
    }

    void* lookup_type(Scope* global_scope)
    {
        return nullptr;
    }

    BasicValue* clone()
    {
        return new BasicValue(this->value);
    }

    std::string toString() const
    {
        std::string result = Util::toString(this->value);
        return result;
    }
};
