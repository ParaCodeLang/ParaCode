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

def DEVSETVERSION(langversion):
    global version
    if dev == True:
        version = langversion
        configFile['version'] = version
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def DEVSETAUTHOR(langauthor):
    global author
    if dev == True:
        author = langauthor
        configFile['author'] = author
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def DEVSETLANGNAME(langname):
    global language_name
    if dev == True:
        language_name = langname
        configFile['language_name'] = language_name
    
        with open("settings.toml", "w+") as f:
            f.write(toml.dumps(configFile))

def PYTHON(args=''):
    os.system('python ' + args)
# def PYTHON():
#     os.system('python')


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
