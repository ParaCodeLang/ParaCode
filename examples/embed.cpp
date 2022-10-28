#include "../src/ParaCode.h"

#include <vector>

void exampleEmbed(ParaCode paraCode) {
    paraCode.callFunction("print", std::vector<["Hello from embed.cpp!"]);
}
