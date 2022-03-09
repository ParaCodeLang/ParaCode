#include "basic_value.h"

namespace Util {
    template<> std::string toString(const BasicValue& t) { return t.toString(); }
}
