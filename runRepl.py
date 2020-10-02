import os

refresh = True

baseInstall = 'pip install'

def combine(install):
    return baseInstall + ' ' + install

if refresh:
    os.system(combine('--upgrade pip'))

    os.system(combine('keyboard'))
    os.system(combine('pynput'))
    os.system(combine('colorama'))
    os.system(combine('colored'))
    os.system(combine('toml'))
    os.system(combine('wget'))
    os.system(combine('bs4'))
    os.system(combine('googletrans'))
    os.system(combine('speechRecognition'))
    os.system(combine('gtts'))

os.system('python shell.py')