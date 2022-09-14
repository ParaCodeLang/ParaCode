#include "../src/ParaCode.h"

void exampleEmbed(ParaCode paraCode) {
    paraCode.callFunction("print", ["Hello from embed.cpp!"]);
}
