import os

version = "1.2.2"
author = "DaRubyMiner360"
language_name = "ParaCode"

debug = False

do_help_command = True

help_command = "HELP"
clear_command = ["CLEAR", "CLR"]
version_command = ["VERSION", "-VERSION", "--VERSION", "ParaCode -VERSION", "ParaCode --VERSION", "PARACODE -VERSION",
                   "PARACODE --VERSION"]


def ECHO(msg='', end='\n'):
    print(msg, end=end)


def PYTHON():
    os.system("python")


def BASH():
    os.system("bash")


def JAVA():
    os.system("java")


def AUTHOR():
    print(author)


def INFO():
    print(language_name, version, "by", author)


def configHelp():
    print(
        """
== Help ==
Here's a list of commands!\n

"""
    )
