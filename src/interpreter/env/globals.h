#pragma once

#include "interpreter/typing/basic_type.h"
#include "interpreter/basic_object.h"
#include "interpreter/variable.h"
#include "interpreter/basic_value.h"
#include "interpreter/function.h"
#include "interpreter/env/builtins.h"

class Globals {
public:
    BasicType* basicType;
    
    Globals() {
        this->basicType = new BasicType(
            nullptr,
            {
                { "name", new BasicValue("Type") },
                { "extend", BuiltinFunction("Type.extend", boost::any(), builtinTypeExtend) },
                // { "type", BuiltinFunction("Type.type", boost::any(), builtinTypeType) },
                // { "is", BuiltinFunction("Type.is", boost::any(), builtinTypeIs) },
                { "to_str", BuiltinFunction("Type.to_str", boost::any(), builtinTypeToStr) },
                // { "new", BuiltinFunction("Object.new", boost::any(), builtinObjectNew) },
            },
            true
        );
    }
};
