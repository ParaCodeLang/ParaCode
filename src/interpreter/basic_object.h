#pragma once

#include "basic_value.h"

#include <boost/any.hpp>

class BasicType;

class ObjectMember {
public:
    std::string name;
    boost::any value;
    
    ObjectMember(std::string name, boost::any value) {
        this->name = name;
        this->value = value;
    }
};

class BasicObject : public BasicValue {
public:
    BasicType* parent;
    std::map<std::string, boost::any> members;
    
    BasicObject(BasicType* parent = nullptr, std::map<std::string, boost::any> members = {}) : BasicValue(nullptr) {
        this->parent = parent;
        this->members = members;
    }
};
