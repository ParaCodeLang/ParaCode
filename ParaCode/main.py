#!/bin/python3

from ParaCode import ParaCode
from parser.parser import Parser
from examples.embed import example_embed

import sys

def main():
    paraCode = ParaCode()

    if len(sys.argv) <= 1:
        paraCode.repl()
        return

    filename = sys.argv[1]
    paraCode.eval_file(filename)

if __name__ == '__main__':
    main()
