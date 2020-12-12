import os
import sys
import platform

buildParaCode = True
buildTest = True

installDependencies = True
installPip = True
runShell = False

args = sys.argv
if len(args) == 2:
    if args[1].lower() == "--installdeps":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runShell = False
        installPip = False
    elif args[1].lower() == "--installpip":
        buildParaCode = False
        buildTest = False
        installDependencies = False
        runShell = False
        installPip = True
    elif args[1].lower() == "--install":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runShell = False
        installPip = True
    elif args[1].lower() == "--installall":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runShell = False
        installPip = True
    elif args[1].lower() == "--buildtest":
        buildParaCode = True
        buildTest = True
        installDependencies = False
        runShell = False
        installPip = False
    elif args[1].lower() == "--build":
        buildParaCode = True
        buildTest = False
        installDependencies = False
        runShell = False
        installPip = False
    elif args[1].lower() == "--runshell":
        buildParaCode = False
        buildTest = False
        installDependencies = False
        runShell = True
        installPip = False

baseInstall = 'pip install'

def combine(install):
    os.system(baseInstall + ' ' + install)
    return baseInstall + ' ' + install

if installPip:
    combine('--upgrade pip')

if installDependencies:
    try:
        import keyboard
    except ImportError:
        combine('keyboard')
    try:
        import pykeyboard
    except ImportError:
        combine('PyUserInput')
    try:
        import pynput
    except ImportError:
        combine('pynput')
    try:
        import colorama
    except ImportError:
        combine('colorama')
    try:
        import colored
    except ImportError:
        combine('colored')
    try:
        import toml
    except ImportError:
        combine('toml')
    try:
        import wget
    except ImportError:
        combine('wget')
    try:
        import bs4
    except ImportError:
        combine('bs4')
    try:
        import googletrans
    except ImportError:
        combine('googletrans')
    try:
        import speech_recognition
    except ImportError:
        combine('speechRecognition')
    try:
        import gtts
    except ImportError:
        combine('gtts')
    try:
        import setuptools
    except ImportError:
        combine('setuptools')
    try:
        import wheel
    except ImportError:
        combine('wheel')
    try:
        import twine
    except ImportError:
        combine('twine')
    try:
        import tqdm
    except ImportError:
        combine('tqdm')
    if platform.system() == "Windows":
        try:
            import win32com
        except ImportError:
            combine('pywin32')
            combine('pyHook')
    elif platform.system() == "Linux":
        try:
            import Xlib
        except ImportError:
            combine('XLib')
    else:
        try:
            import Quartz
        except ImportError:
            combine('Quartz')
            combine('AppKit')
    try:
        import discord
    except ImportError:
        combine('discord')
        combine('discord.py')
    try:
        import dotenv
    except ImportError:
        combine('python-dotenv')

    combine('-i https://test.pypi.org/simple/ ParaCode')

if buildParaCode:
    if buildTest:
        os.system('python setup.py sdist bdist_wheel')
        os.system('python -m twine upload --repository testpypi dist/*')
    else:
        os.system('python setup.py sdist bdist_wheel')
        os.system('python -m twine upload dist/*')

if runShell:
    os.system('python shell.py')