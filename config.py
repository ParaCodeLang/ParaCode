import os
import toml

configFile = toml.load("settings.toml")

dev = configFile.get("dev")

version = configFile.get("version")
author = configFile.get("author")
language_name = configFile.get("language_name")

debug = False

do_help_command = True

returned = False

help_command = "HELP"
clear_command = ["CLEAR", "CLR"]
version_command = ["VERSION", "-VERSION", "--VERSION", "ParaCode -VERSION", "ParaCode --VERSION", "PARACODE -VERSION",
                   "PARACODE --VERSION"]


def ECHO(msg='', end='\n'):
    print(msg, end=end)

def DEVSETVERSION(langversion):
    if dev == True:
        version = langversion
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def DEVSETAUTHOR(langauthor):
    if dev == True:
        author = langauthor
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def DEVSETLANGNAME(langname):
    if dev == True:
        language_name = langname
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def PYTHON(args=''):
    os.system('python ' + args)


def BASH(args=''):
    os.system('bash ' + args)


def JAVA(args=''):
    os.system('java ' + args)

def GO(args=''):
    os.system('go ' + args)


def AUTHOR():
    print(author)


def INFO():
    print(language_name, version, "by", author)

def REFRESH():
    os.system("python shell.py")

def EXIT():
    returned = True


def configHelp():
    print(
        """
== Help ==
Here's a list of commands!\n

"""
    )
