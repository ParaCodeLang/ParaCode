#pragma once

#include "interpreter/basic_object.h"

#include <boost/any.hpp>

class BasicType : public BasicObject {
public:
    static std::string REPR_FUNCTION_NAME;

    bool nominative;
    
    BasicType(BasicType* parent = nullptr, std::map<std::string, boost::any> members = {}, bool nominative = true) : BasicObject(parent, members) {
        this->nominative = nominative;
    }

    boost::any typeName() {
        return this->members["name"];
    }

    std::string friendlyTypename() {
        if (this->members.count("name")) {
            if (Util::isType<BasicValue>(this->members["name"])) {
                return boost::any_cast<std::string>(boost::any_cast<BasicValue*>(this->members["name"])->extractValue());
            }
            else {
                return boost::any_cast<std::string>(this->members["name"]);
            }
        }

        return this->toString();
    }

    bool compareType(BasicType* otherType, bool parentLookup = true) {
        if (otherType == this) {
            return true;
        }

        if (this->compareValue(otherType)) {
            return true;
        }

        if (parentLookup && this->parent != nullptr) {
            bool circular = otherType->parent->parent == otherType;

            return this->compareType(otherType->parent, !circular);
        }

        return false;
    }

    bool hasProperty(std::string name, boost::any propertyType = boost::any(), bool limit = false) {
        if (this->members.count(name)) {
            return true;
        }

        if (limit || this->parent == nullptr) {
            return false;
        }

        return this->parent->hasProperty(name, propertyType);
    }

    boost::any getPropertyType(std::string name, bool limit = false) {
        if (this->members.count(name)) {
            return this->members[name];
        }

        if (limit || this->parent == nullptr) {
            return boost::any();
        }

        return this->parent->getPropertyType(name);
    }

    virtual std::string toString() const override {
        return Util::format("BasicType(%s)", Util::toString(this->members).c_str());
    }
};
