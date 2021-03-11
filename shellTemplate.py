#!/bin/python3

import os
from ParaCode import ParaCode
from parse.parser import Parser

import sys

def main():
    os.system("")

    paraCode = ParaCode()

    filename = str(os.path.join(sys._MEIPASS, "shellTemplate.para")).replace('\\', '/')
    paraCode.eval_file(filename)


if __name__ == '__main__':
    main()
