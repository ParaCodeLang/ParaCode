#include "basic_value.h"

ObjectMember* BasicObject::lookupMember(std::string name, boost::any memberType, bool parentLookup) {
    if (this->members.count(name)) {
        if (memberType.empty() || boost::any_cast<BasicObject*>(this->members[name]).satisfiesType(memberType)) {
            return new ObjectMember(name, this->members[name]);
        }
    }
    //else if (name == "type") {
    //    return new ObjectMember("type", this->parent);
    //}
    else if (parentLookup && this->parent != nullptr) {
        bool circular = this->parent->parent == this;

        return this->parent->lookupMember(name, memberType, parentLookup && !circular);
    }

    return nullptr;
}
