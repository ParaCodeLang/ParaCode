#include <stdio.h>
#include <string>

// import os
#include "ParaCode.h"
from parse.parser import Parser
from examples.embed import example_embed

import sys

int main(int argc, char** argv) {
    // os.system("");

    ParaCode paraCode = new ParaCode();

    if (argc <= 1):
        paraCode.repl();
        return 0;

    string filename = argv[1];
    paraCode.eval_file(filename);

    return 0;
}
