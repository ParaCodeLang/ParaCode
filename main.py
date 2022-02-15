#!/bin/python3

import sys

# TODO: Implement version checker with `vermin --backport enum --no-parse-comments --versions .`

import os
from ParaCode import ParaCode
from parse.parser import Parser

# TODO: Move installDependencies.py and dataCounter.py's code here

def main():
    os.system("")

    paraCode = ParaCode()

    if len(sys.argv) <= 1:
        paraCode.repl()
        return

    filename = sys.argv[1]
    paraCode.eval_file(filename)


if __name__ == '__main__':
    main()
