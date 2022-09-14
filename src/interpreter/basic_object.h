#pragma once

#include "basic_value.h"

#include <boost/any.hpp>

class BasicType;
class UnionType;

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

    boolean compareValue(BasicObject* other) override {
        if (other == this) {
            return true;
        }

        if (!Util::isType<BasicObject>(other)) {
            return false;
        }

        for (auto& item : this->members) {
            std::string memName = item.first;
            BasicValue* memValue = boost::any_cast<BasicValue*>(item.second);
            ObjectMember* objectMember = other->lookupMember(memName);

            if (objectMember == nullptr) {
                return false;
            }

            if (!memValue.compareValue(objectMember->value)) {
                return false;
            }
        }
        
        return true;
    }

    BasicValue* extractValue() override {
        return this;
    }

    BasicValue* extractBasicvalue() override {
        return this;
    }

    BasicValue* lookupType(Scope* globalScope) {
        if (this->parent != nullptr) {
            return this->parent;
        }

        // BasicValue lookupType call - resolves to Object usually
        return BasicValue::lookupType(globalScope);
    }

    BasicValue* clone(parentOverride) {
        BasicType* parent = this->parent;

        if (parentOverride != nullptr) {
            parent = parentOverride;
        }

        std::map<std::string, boost::any> members = {};

        for (auto& item : this->members) {
            std::string key = item.first;
            boost::any value = item.second;
            
            if (Util::isType<BasicValue>(value)) {
                members[key] = boost::any_cast<BasicValue*>(value)->clone();
            }
            else {
                members[key] = value; // this should actually just throw eventually unless it's a NodeFunctionExpression.
            }
        }

        return new BasicObject(parent, members);
    }

    BasicValue* clone() override {
        return clone(nullptr);
    }

    void assignMember(std::string name, boost::any value) {
        this->members[name] = value;
    }

    ObjectMember* lookupMember(std::string name, boost::any memberType=boost::any(), bool parentLookup=true);

    bool satisfiesType(boost::any type) {
        // all members are str -> BasicObject (or an extension thereof)
        for (auto& item : type.members) {
            std::string tname = item.first;
            boost::any tvalue = item.second;
            
            if (this->lookupMember(tname, tvalue) == nullptr) {
                return false;
            }
        }

        if (type->parent != nullptr) {
            return this->satisfiesType(type->parent);
        }

        return true;
    }

    def union(other) {
        unionMembers = self.members.copy();

        for ((name, value) in other.members.items()) {
            if (name in unionMembers) {
                if (not value.compareValue(unionMembers[name])) {
                    unionMembers[name] = new UnionType(unionMembers[name], value);
                }
            }
        }
        else {
            unionMembers[name] = value;
        }

        return new BasicObject(nullptr, unionMembers);
    }
};
