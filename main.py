#!/bin/python3

import os
from ParaCode import ParaCode
from parse.parser import Parser
from examples.embed import example_embed

import sys

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
