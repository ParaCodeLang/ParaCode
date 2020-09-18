import os

version = "1.1.6"
author = "DaRubyMiner360"
language_name = "ParaCode"

do_help_command = True  # use the built-in help command?

help_command = "HELP"
clear_command = ["CLEAR", "CLR"]  # you can have aliases to the command
version_command = ["VERSION", "-VERSION", "--VERSION", "ParaCode -VERSION", "ParaCode --VERSION", "PARACODE -VERSION", "PARACODE --VERSION"]  # you can have aliases to the command

def ECHO(msg='',end='\n'):
    print(msg,end=end)

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
== Help Manual ==
Hello, welcome to the help manual!\n
\n
Lets get started on creating your interpreter (console)!\n
\n
First step is to configurate it to your own preference!\n
To go this, go to main.py and change the variables in the configuration.\n
! DONT CHANGE THE COMPILER'S CODE UNLESS YOU KNOW WHAT YOU ARE DOING!\n
\n
Next step is to start creating the commands!\n
Go to config.py and delete all the premade functions in it if you want.\n
The commands are just functions in python and the parameters are function parameters!\n
\n
Have fun!\n
Don't forget to share your interpreter in the comments below, hope to see what you guys make!
"""
)