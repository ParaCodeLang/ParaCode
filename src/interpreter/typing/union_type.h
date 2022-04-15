#pragma once

#include "interpreter/basic_type.h"

#include <boost/any.hpp>

class UnionType : public BasicType {
public:
    BasicType* lhs;
    BasicType* rhs;
    
    UnionType(BasicType* lhs, BasicType* rhs) : BasicType(nullptr, {}, false) {
        this->lhs = lhs;
        this->rhs = rhs;
    }

    bool compareValue(BasicType* otherType) {
        return this->lhs->compareValue(otherType) || this->rhs->compareValue(otherType);
    }

    bool hasProperty(self, name, property_type=None) {
        return self.lhs.has_property(name, property_type) or self.rhs.has_property(name, property_type)
    }

    boost::any getPropertyType(std::string name) {
        if (this->lhs->hasProperty(name)) {
            if (this->rhs->hasProperty(name)) {
                return UnionType(this->lhs->getPropertyType(name), this->rhs->getPropertyType(name));
            }
            else {
                return this->lhs->getPropertyType(name);
            }
        }

        if (this->rhs->hasProperty(name)) {
            return this->rhs->getPropertyType(name);
        }

        return boost::any();
    }

    std::string toString() {
        return Util::format("UnionType(%s, %s)", Util::toString(this->lhs).c_str(), Util::toString(this->rhs).c_str());
    }
};
