#pragma once

#include "interpreter/basic_value.h"

#include <chrono>
#include <thread>
#include <ctime>

BasicValue* builtinTimeSleep(BuiltinFunctionArguments arguments) {
    int ms = boost::any_cast<int>(arguments.arguments[0].extractValue());
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    return new BasicValue(ms);
}

BasicValue* builtinTimeNow(BuiltinFunctionArguments arguments) {
    int timeEpoch = (int) std::time(nullptr);
    return new BasicValue(timeEpoch);
}

