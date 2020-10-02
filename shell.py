import platform

import keyboard as keyb
from inspect import signature as sign, isfunction as func
if platform.system() == "Windows":
    import win32com.client
    from pynput.keyboard import Key, Controller
from ctypes import *

import signal

# from replit import db

import sys

import toml
import os
import urllib
from json import loads as parse, dumps as stringify
import json

import requests
import wget
from bs4 import BeautifulSoup

import basic
import config

from colorama import init
from colorama import Fore as coloramaFore
from colorama import Back as coloramaBack
from colorama import Style as coloramaStyle
from colored import fore as Fore
from colored import back as Back
from colored import fg as Fg
from colored import bg as Bg
from colored import attr as Attr

import time

returned = config.returned

used = 0
executed = 0
originalSigInt = signal.getsignal(signal.SIGINT)
originalStdout = sys.stdout
canSubmit = True
debug = config.debug

# -- Configuration (Settings) -- #
configFile = toml.load("config.toml")

user_color = configFile.get("shell").get("userColor")
user_style = configFile.get("shell").get("userStyle")
console_color = configFile.get("shell").get("consoleColor")
console_style = configFile.get("shell").get("consoleStyle")

pointer = "ParaCode Shell >>>"
pointer_color = configFile.get("shell").get("pointerColor")
pointer_style = configFile.get("shell").get("pointerStyle")

error_color = configFile.get("shell").get("errorColor")
error_style = configFile.get("shell").get("errorStyle")


# {} is the command given by the user
class error:
    syntax_error = "Error: '{}' is not a valid command."
    name_error = "Error: '{}' is not defined."
    type_error = "Error: wrong type for '{}'"
    invalid_parameter_error = "Error: {required_params} required parameters required and {optional_params} optional " \
                              "parameters needed but {params_given} given. "


class errorfx:
    syntax_error = "Error: '{}' is not a valid command."
    name_error = "Error: '{}' is not defined."
    type_error = "Error: wrong type for '{}'"
    invalid_parameter_error = "Error: {required_params} required parameters required and {optional_params} optional " \
                              "parameters needed but {params_given} given. "


do_help_command = config.do_help_command
help_command = config.help_command

version = config.version
language_name = config.language_name
author = config.author

clear_command = config.clear_command
version_command = config.version_command

stopped = 0

sytling = {
    "white": coloramaFore.WHITE,
    "red": coloramaFore.RED,
    "green": coloramaFore.GREEN,
    "blue": coloramaFore.BLUE,
    "purple": coloramaFore.MAGENTA,
    "cyan": coloramaFore.CYAN,
    "orange": coloramaFore.YELLOW,
    "yellow": coloramaFore.YELLOW,
    "magenta": coloramaFore.MAGENTA,
    "bright_black": coloramaFore.LIGHTBLACK_EX,
    "bright_red": coloramaFore.LIGHTRED_EX,
    "bright_green": coloramaFore.LIGHTGREEN_EX,
    "bright_yellow": coloramaFore.LIGHTYELLOW_EX,
    "bright_blue": coloramaFore.LIGHTBLUE_EX,
    "bright_magenta": coloramaFore.LIGHTMAGENTA_EX,
    "bright_cyan": coloramaFore.LIGHTCYAN_EX,
    "bright_white": coloramaFore.LIGHTWHITE_EX,
    "brightBlack": coloramaFore.LIGHTBLACK_EX,
    "brightRed": coloramaFore.LIGHTRED_EX,
    "brightGreen": coloramaFore.LIGHTGREEN_EX,
    "brightYellow": coloramaFore.LIGHTYELLOW_EX,
    "brightBlue": coloramaFore.LIGHTBLUE_EX,
    "brightMagenta": coloramaFore.LIGHTMAGENTA_EX,
    "brightCyan": coloramaFore.LIGHTCYAN_EX,
    "brightWhite": coloramaFore.LIGHTWHITE_EX,
    "brightblack": coloramaFore.LIGHTBLACK_EX,
    "brightred": coloramaFore.LIGHTRED_EX,
    "brightgreen": coloramaFore.LIGHTGREEN_EX,
    "brightyellow": coloramaFore.LIGHTYELLOW_EX,
    "brightblue": coloramaFore.LIGHTBLUE_EX,
    "brightmagenta": coloramaFore.LIGHTMAGENTA_EX,
    "brightcyan": coloramaFore.LIGHTCYAN_EX,
    "brightwhite": coloramaFore.LIGHTWHITE_EX,
    "underline": "\033[04m",
    "italic": "\033[03m",
    "darken": "\033[02m",
    "invisible": "\033[08m",
    "reverse": "\033[07m",
    "reset": "\033[0m",
    "normal": coloramaStyle.NORMAL,
    "reset_all": coloramaStyle.RESET_ALL,
    "resetAll": coloramaStyle.RESET_ALL,
    "resetall": coloramaStyle.RESET_ALL,
    "bright": coloramaStyle.BRIGHT,
    "dim": coloramaStyle.DIM,
    "none": "",
    "": "",
    "bgwhite": coloramaBack.WHITE,
    "bgred": coloramaBack.RED,
    "bggreen": coloramaBack.GREEN,
    "bgblue": coloramaBack.BLUE,
    "bgpurple": coloramaBack.MAGENTA,
    "bgcyan": coloramaBack.CYAN,
    "bgorange": coloramaBack.YELLOW,
    "bgyellow": coloramaBack.YELLOW,
    "bgmagenta": coloramaBack.MAGENTA,
    "bgbright_black": coloramaBack.LIGHTBLACK_EX,
    "bgbright_red": coloramaBack.LIGHTRED_EX,
    "bgbright_green": coloramaBack.LIGHTGREEN_EX,
    "bgbright_yellow": coloramaBack.LIGHTYELLOW_EX,
    "bgbright_blue": coloramaBack.LIGHTBLUE_EX,
    "bgbright_magenta": coloramaBack.LIGHTMAGENTA_EX,
    "bgbright_cyan": coloramaBack.LIGHTCYAN_EX,
    "bgbright_white": coloramaBack.LIGHTWHITE_EX,
    "bgbrightBlack": coloramaBack.LIGHTBLACK_EX,
    "bgbrightRed": coloramaBack.LIGHTRED_EX,
    "bgbrightGreen": coloramaBack.LIGHTGREEN_EX,
    "bgbrightYellow": coloramaBack.LIGHTYELLOW_EX,
    "bgbrightBlue": coloramaBack.LIGHTBLUE_EX,
    "bgbrightMagenta": coloramaBack.LIGHTMAGENTA_EX,
    "bgbrightCyan": coloramaBack.LIGHTCYAN_EX,
    "bgbrightWhite": coloramaBack.LIGHTWHITE_EX,
    "bgbrightblack": coloramaBack.LIGHTBLACK_EX,
    "bgbrightred": coloramaBack.LIGHTRED_EX,
    "bgbrightgreen": coloramaBack.LIGHTGREEN_EX,
    "bgbrightyellow": coloramaBack.LIGHTYELLOW_EX,
    "bgbrightblue": coloramaBack.LIGHTBLUE_EX,
    "bgbrightmagenta": coloramaBack.LIGHTMAGENTA_EX,
    "bgbrightcyan": coloramaBack.LIGHTCYAN_EX,
    "bgbrightwhite": coloramaBack.LIGHTWHITE_EX
}

os.system('cls' if os.name == 'nt' else 'clear')

def e(c):
    exec('global i; i = %s' % c)
    global i
    return i


try:
    if user_color.startswith('#'):
        user_color = Fg(user_color)
    else:
        user_color = sytling[user_color]
    
    if user_style.startswith('#'):
        user_style = Fg(user_style)
    else:
        user_style = sytling[user_style]
    
    if console_color.startswith('#'):
        console_color = Fg(console_color)
    else:
        console_color = sytling[console_color]
    
    if console_style.startswith('#'):
        console_style = Fg(console_style)
    else:
        console_style = sytling[console_style]
    
    if pointer_color.startswith('#'):
        pointer_color = Fg(pointer_color)
    else:
        pointer_color = sytling[pointer_color]
    
    if pointer_style.startswith('#'):
        pointer_style = Fg(pointer_style)
    else:
        pointer_style = sytling[pointer_style]
    
    if error_color.startswith('#'):
        error_color = Fg(error_color)
    else:
        error_color = sytling[error_color]
    
    if error_style.startswith('#'):
        error_style = Fg(error_style)
    else:
        error_style = sytling[error_style]
except:
    print("\033[31mInvalid colors in configuration.\033[0m")

if do_help_command:
    print((Fg('#00ff1f') + "{} {} [{}] 2020 (c)\n" + Fg('#c400ff') + "Type HELP, CREDITS, or LICENSE for more information." + Attr('reset')).format(language_name, version,
                                                                                             author))
else:
    print((Fg('#c400ff') + "{} {} [{}] 2020 (c)\nType CREDITS, or LICENSE for more information." + Attr('reset')).format(language_name, version, author))
help = '== Help ==\nFor help with a command, type HELP [command]'


def Run(command):
    global debug, packageRegistryName, executed, used
    global error
    global errorfx
    while (stopped == 0 or stopped == 2) and returned == False:
        if executed == 0:
            if command is not None and command != "":
                text = command
            else:
                text = ""
                try:
                    print("")
                    text = input(pointer_color + pointer_style + pointer + console_color + console_style + " ")
                except:
                    pass
            if text.strip() == "":
                continue
            text = text.replace('\\', '/')
            if debug:
                print(text)
            if text.startswith(help_command + " ") and do_help_command:
                text = text.split(help_command + " ")[1]
                try:
                    if func(e("config." + text)):
                        print("== Help | " + text + " ==")
                        h = []
                        prm = [0, 0]
                        co = 0
                        sig = sign(e("config." + text.split(" ")[0]))
                        for key in list(dict(sig.parameters).keys()):
                            if str(dict(sig.parameters)[key]).startswith("{}=".format(key)):
                                prm[1] += 1
                            else:
                                prm[0] += 1
                        for i in str(sign(e("config." + text)))[1:-1].split(", "):
                            if co <= prm[0]:
                                h.append("[" + i.split("=")[0] + "]")
                            else:
                                h.append("(" + i.split("=")[0] + ")")
                            co += 1
                        print("Usage: " + text + " " + ' '.join(h) + "\nParams: " + " | ".join(
                            str(sign(e("config." + text)))[1:-1].split(",")))
                except:
                    print(error_color + error_style + error.syntax_error.format(text))
            elif text == help_command:
                print("== Help ==\nFor help with a command, type help [command]")
            elif StartsWith(text, "PCPM "):
                string = text.replace("pcpm ", "", 1).replace("PCPM ", "", 1)
                if StartsWith(string, "INSTALL "):
                    string = string.replace("install ", "", 1).replace("INSTALL ", "", 1)
                    if StartsWith(string, "PyGithub "):
                        string = string.replace("pygithub ", "", 1).replace("PYGITHUB ", "", 1).replace("PyGithub ", "",
                                                                                                        1)

                        # TODO: Implement PyGithub
                    elif StartsWith(string, "Requests "):
                        string = string.replace("requests ", "", 1).replace("REQUESTS ", "", 1).replace("Requests ", "",
                                                                                                        1)

                        URL = string

                        r = requests.get(URL)
                        soup = BeautifulSoup(r.content, "html5lib")
                        if not URL.replace("/", "").endswith(".para") and not URL.replace("/", "").endswith(
                                ".paracode") and not URL.replace("/", "").endswith(".md") and not URL.replace("/",
                                                                                                              "").endswith(
                            ".json"):
                            count = 0

                            links = soup.findAll("a")
                            linkList = [URL + link["href"] for link in links if
                                        link["href"].endswith(".para") or link["href"].endswith(".paracode") or link[
                                            "href"].endswith(".md") or link["href"].endswith(".json") or StartsWith(
                                            link["href"], "LICENSE")]
                            for link in linkList:
                                if "https://github.com" in link:
                                    slash = link.split("/")[3]
                                    slash2 = link.split("/")[4]
                                    link = link.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                        "https://github.com", "https://raw.githubusercontent.com").replace("/blob/",
                                                                                                           "/")
                                fileName = link.split("/")[-1]

                                packageSrcDir2 = ""
                                packageRegistryName2 = ""
                                packageLink = ""
                                r22 = ""
                                if any("ParaPackage.json" in s for s in linkList):
                                    if "ParaPackage.json" in link:
                                        file = urllib.request.urlopen(link)

                                        jsonCode = ""

                                        for line in file:
                                            decoded_line = line.decode("utf-8")
                                            print(decoded_line)
                                            jsonCode = jsonCode + decoded_line
                                            print(jsonCode)
                                        else:
                                            dic = json.loads(jsonCode)
                                            packageRegistryName = dic['registryName']
                                            packageSrcDir = dic['srcDir']
                                            packageName = dic['name']
                                            packageVersion = dic['version']
                                            packageDescription = dic['description']

                                            packageSrcDir2 = packageSrcDir
                                            packageRegistryName2 = packageRegistryName
                                            print(packageRegistryName)
                                            print(packageSrcDir)
                                            print(packageName)
                                            print(packageVersion)
                                            print(packageDescription)

                                            r2 = requests.get(URL + packageSrcDir)
                                            soup2 = BeautifulSoup(r2.content, "html5lib")
                                            links2 = soup.findAll("a")
                                            linkList2 = [URL + "/" + "" + link2["href"] for link2 in links2 if
                                                         link2["href"].endswith(".para") or link2["href"].endswith(
                                                             ".paracode") or
                                                         link2[
                                                             "href"].endswith(".md") or link2["href"].endswith(
                                                             ".json") or StartsWith(
                                                             link2["href"], "LICENSE")]
                                            if os.path.exists(
                                                    os.path.realpath(__file__).replace("shell.py", "") + configFile.get(
                                                        "lang").get(
                                                        "packagePath") + packageRegistryName + "\\" + fileName):
                                                with open(os.path.realpath(__file__).replace("shell.py",
                                                                                             "") + configFile.get(
                                                    "lang").get("packagePath") + packageRegistryName + "\\" + fileName,
                                                          "wb") as f:
                                                    r3 = requests.get(link)
                                                    for chunk in r3.iter_content(chunk_size=1024 * 1024):
                                                        if chunk:
                                                            f.write(chunk)
                                                    print(f"Successfully downloaded {fileName}!")
                                                    count += 1
                                            else:
                                                os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                            "") + configFile.get(
                                                    "lang").get("packagePath") + packageRegistryName)
                                                os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                            "") + configFile.get(
                                                    "lang").get(
                                                    "packagePath") + packageRegistryName + "\\" + packageSrcDir2)
                                                with open(os.path.realpath(__file__).replace("shell.py",
                                                                                             "") + configFile.get(
                                                    "lang").get("packagePath") + packageRegistryName + "\\" + fileName,
                                                          "wb") as f:
                                                    r3 = requests.get(link)
                                                    for chunk in r3.iter_content(chunk_size=1024 * 1024):
                                                        if chunk:
                                                            f.write(chunk)
                                                    print(f"Successfully downloaded {fileName}!")
                                                    count += 1

                                        data = {}
                                        data['packages'].append({
                                            "registryName": packageRegistryName,
                                            "installedVersion": packageVersion,
                                            "enabled": True,
                                            "location": packageRegistryName + "/"
                                        })

                                        if os.path.exists(os.path.realpath(__file__).replace("shell.py",
                                                                                             "") + configFile.get(
                                            "lang").get("packagePath") + packageRegistryName + "\\" + fileName):
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get("packagePath") + "Packages.json",
                                                      'a') as outfile:
                                                json.dump(data, outfile)
                                        else:
                                            os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                        "") + "Packages")
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get("packagePath") + "Packages.json",
                                                      'a') as outfile:
                                                json.dump(data, outfile)
                                    elif ".md" in fileName or "license" in fileName or "LICENSE" in fileName:
                                        print(f"Downloading file: {fileName}!")
                                        if os.path.exists(os.path.realpath(__file__).replace("shell.py",
                                                                                             "") + configFile.get(
                                            "lang").get("packagePath") + packageRegistryName + "\\" + fileName):
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get("packagePath") + packageRegistryName2 + "\\" + fileName,
                                                      "wb") as f:
                                                r2 = requests.get(link)
                                                for chunk in r2.iter_content(chunk_size=1024 * 1024):
                                                    if chunk:
                                                        f.write(chunk)
                                                print(f"Successfully downloaded {fileName}!")
                                                count += 1
                                        else:
                                            os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                        "") + configFile.get(
                                                "lang").get("packagePath") + packageRegistryName)
                                            os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                        "") + configFile.get(
                                                "lang").get(
                                                "packagePath") + packageRegistryName + "\\" + packageSrcDir2)
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get("packagePath") + packageRegistryName2 + "\\" + fileName,
                                                      "wb") as f:
                                                r2 = requests.get(link)
                                                for chunk in r2.iter_content(chunk_size=1024 * 1024):
                                                    if chunk:
                                                        f.write(chunk)
                                                print(f"Successfully downloaded {fileName}!")
                                                count += 1
                                    else:
                                        print(f"Downloading file: {fileName}!")
                                        packageLink = link.replace(packageSrcDir2, "")
                                        r22 = requests.get(packageLink + packageSrcDir2)

                                        if os.path.exists(os.path.realpath(__file__).replace("shell.py",
                                                                                             "") + configFile.get(
                                            "lang").get("packagePath") + packageRegistryName + "\\" + fileName):
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get(
                                                "packagePath") + packageRegistryName2 + "\\" + packageSrcDir2 + fileName,
                                                      "wb") as f:
                                                for chunk in r22.iter_content(chunk_size=1024 * 1024):
                                                    if chunk:
                                                        f.write(chunk)
                                                print(f"Successfully downloaded {fileName}!")
                                                count += 1
                                        else:
                                            os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                        "") + configFile.get(
                                                "lang").get("packagePath") + packageRegistryName)
                                            os.mkdir(os.path.realpath(__file__).replace("shell.py",
                                                                                        "") + configFile.get(
                                                "lang").get(
                                                "packagePath") + packageRegistryName + "\\" + packageSrcDir2)
                                            with open(os.path.realpath(__file__).replace("shell.py",
                                                                                         "") + configFile.get(
                                                "lang").get(
                                                "packagePath") + packageRegistryName2 + "\\" + packageSrcDir2 + fileName,
                                                      "wb") as f:
                                                for chunk in r22.iter_content(chunk_size=1024 * 1024):
                                                    if chunk:
                                                        f.write(chunk)
                                                print(f"Successfully downloaded {fileName}!")
                                                count += 1
                            else:
                                if count != 1:
                                    print(f"Successfully downloaded {count} files!")
                                else:
                                    print(f"Successfully downloaded {count} file!")
                        else:
                            with open(os.path.realpath(__file__).replace("shell.py", "") + URL.split("/")[-1],
                                      "wb") as f:
                                fileName = URL.split("/")[-1]
                                if "https://github.com" in URL:
                                    slash = URL.split("/")[3]
                                    slash2 = URL.split("/")[4]
                                    URL = URL.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                        "https://github.com", "https://raw.githubusercontent.com").replace("/blob/",
                                                                                                           "/")
                                    r = requests.get(URL)
                                print(f"Downloading file: {fileName}!")
                                f.write(r.content)
                                print(f"Successfully downloaded {fileName}!")
                    elif StartsWith(string, "WGet "):
                        string = string.replace("wget ", "", 1).replace("WGET ", "", 1).replace("WGet ", "", 1).replace(
                            "Wget ", "", 1)

                        URL = string
                        if not URL.replace("/", "").endswith(".para") and not URL.replace("/", "").endswith(
                                ".paracode") and not URL.replace("/", "").endswith(".md"):
                            string = string

                            # TODO: Implement Multiple Files With WGet
                        else:
                            if "https://github.com" in URL:
                                slash = URL.split("/")[3]
                                slash2 = URL.split("/")[4]
                                URL = URL.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                    "https://github.com", "https://raw.githubusercontent.com").replace("/blob/", "/")
                            print(f"Downloading file: {fileName}!")
                            wget.download(URL, os.path.realpath(__file__).replace("shell.py", "") + URL.split("/")[-1])
                            print(f"Successfully downloaded {fileName}!")
                    elif StartsWith(string, "URLLib "):
                        string = string.replace("urllib ", "", 1).replace("URLLIB ", "", 1).replace("URLLib ", "",
                                                                                                    1).replace(
                            "URLlib ", "", 1)

                        URL = string
                        r = requests.get(URL)
                        soup = BeautifulSoup(r.content, "html5lib")
                        if not URL.replace("/", "").endswith(".para") and not URL.replace("/", "").endswith(
                                ".paracode") and not URL.replace("/", "").endswith(".md") and not URL.replace("/",
                                                                                                              "").endswith(
                            ".json"):
                            count = 0

                            links = soup.findAll("a")
                            linkList = [URL + link["href"] for link in links if
                                        link["href"].endswith(".para") or link["href"].endswith(".paracode") or link[
                                            "href"].endswith(".md") or link["href"].endswith(".json") or StartsWith(
                                            link["href"], "LICENSE")]
                            for link in linkList:
                                if "https://github.com" in link:
                                    slash = link.split("/")[3]
                                    slash2 = link.split("/")[4]
                                    link = link.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                        "https://github.com", "https://raw.githubusercontent.com").replace("/blob/",
                                                                                                           "/")
                                fileName = link.split("/")[-1]
                                print(f"Downloading file: {fileName}!")
                                urllib.request.urlretrieve(link,
                                                           os.path.realpath(__file__).replace("shell.py", "") +
                                                           link.split("/")[
                                                               -1])
                                print(f"Successfully downloaded {fileName}!")
                                count += 1
                            if count != 1:
                                print(f"Successfully downloaded {count} files!")
                            else:
                                print(f"Successfully downloaded {count} file!")
                        else:
                            fileName = URL.split("/")[-1]
                            if "https://github.com" in URL:
                                slash = URL.split("/")[3]
                                slash2 = URL.split("/")[4]
                                URL = URL.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                    "https://github.com", "https://raw.githubusercontent.com").replace("/blob/", "/")
                            print(f"Downloading file: {fileName}!")
                            urllib.request.urlretrieve(URL,
                                                       os.path.realpath(__file__).replace("shell.py", "") +
                                                       URL.split("/")[
                                                           -1])
                            print(f"Successfully downloaded {fileName}!")
                    else:
                        URL = string

                        r = requests.get(URL)
                        soup = BeautifulSoup(r.content, "html5lib")
                        if not URL.replace("/", "").endswith(".para") and not URL.replace("/", "").endswith(
                                ".paracode") and not URL.replace("/", "").endswith(".md"):
                            count = 0

                            links = soup.findAll("a")
                            linkList = [URL + link["href"] for link in links if
                                        link["href"].endswith(".para") or link["href"].endswith(".paracode") or link[
                                            "href"].endswith(".md") or link["href"].endswith(".json") or StartsWith(
                                            link["href"], "LICENSE")]
                            for link in linkList:
                                if "https://github.com" in link:
                                    slash = link.split("/")[3]
                                    slash2 = link.split("/")[4]
                                    link = link.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                        "https://github.com", "https://raw.githubusercontent.com").replace("/blob/",
                                                                                                           "/")
                                fileName = link.split("/")[-1]
                                print(f"Downloading file: {fileName}!")
                                with open(os.path.realpath(__file__).replace("shell.py", "") + fileName, "wb") as f:
                                    r2 = requests.get(link)
                                    for chunk in r2.iter_content(chunk_size=1024 * 1024):
                                        if chunk:
                                            f.write(chunk)
                                    print(f"Successfully downloaded {fileName}!")
                                    count += 1
                            if count != 1:
                                print(f"Successfully downloaded {count} files!")
                            else:
                                print(f"Successfully downloaded {count} file!")
                        else:
                            with open(os.path.realpath(__file__).replace("shell.py", "") + URL.split("/")[-1],
                                      "wb") as f:
                                fileName = URL.split("/")[-1]
                                if "https://github.com" in URL:
                                    slash = URL.split("/")[3]
                                    slash2 = URL.split("/")[4]
                                    URL = URL.replace(slash + "/", "", 1).replace(slash2 + "/", "", 1).replace(
                                        "https://github.com", "https://raw.githubusercontent.com").replace("/blob/",
                                                                                                           "/")
                                    r = requests.get(URL)
                                print(f"Downloading file: {fileName}!")
                                f.write(r.content)
                                print(f"Successfully downloaded {fileName}!")
            elif text == "LICENSE":
                print("""Copyright (c) 2020 {}

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.""".format(author))
            elif text == "CREDITS":
                print(
                    "Thank you to DaRubyMiner360 creating and developing ParaCode!")
            elif text in version_command:
                print("ParaCode", version)
            elif text in clear_command:
                # print("\033c", end="", flush=True)
                os.system('cls' if os.name == 'nt' else 'clear')
                if do_help_command:
                    print("{} {} [{}] 2020 (c)\nType HELP, CREDITS, or LICENSE for more information.".format(
                        language_name,
                        version,
                        author))
                else:
                    print(
                        "{} {} [{}] 2020 (c)\nType CREDITS, or LICENSE for more information.".format(language_name,
                                                                                                     version,
                                                                                                     author))
            elif text == "DEBUG":
                startDebug = debug
                debug = True

                run = ""

                preferencesFile = "preferences.toml"
                file_exists = os.path.isfile(preferencesFile)

                if file_exists:
                    preferences = toml.load(preferencesFile)

                    lastRun = preferences.get('lastRun')
                    if lastRun.endswith(".para") or lastRun.endswith(".paracode"):
                        run = lastRun
                else:
                    run = ""
                if run != "":
                    newText = 'RUN("' + run + '")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
                    debug = startDebug
                else:
                    newText = 'RUN("main.para")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
                    newText = 'RUN("main.paracode")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
                    debug = startDebug
            elif text == "TOGGLEDEBUG":
                if debug:
                    debug = False
                    print("DEBUG: FALSE")
                else:
                    debug = True
                    print("DEBUG: TRUE")
            elif text == "TESTBUG" or text == "TESTDEBUG" or text == "DEBUGTEST":
                startDebug = debug
                debug = True
                newText = 'RUN("test.para")'
                result, error = basic.run('<stdin>', newText)
                if debug:
                    print(newText)
                newText = 'RUN("test.paracode")'
                result, error = basic.run('<stdin>', newText)
                if debug:
                    print(newText)
                debug = startDebug
            elif text == "TEST":
                newText = 'RUN("test.para")'
                result, error = basic.run('<stdin>', newText)
                if debug:
                    print(newText)
                newText = 'RUN("test.paracode")'
                result, error = basic.run('<stdin>', newText)
                if debug:
                    print(newText)
            elif text == "RUN":
                run = ""

                preferencesFile = "preferences.toml"
                file_exists = os.path.isfile(preferencesFile)

                if file_exists:
                    preferences = toml.load(preferencesFile)

                    lastRun = preferences.get('lastRun')
                    if lastRun.endswith(".para") or lastRun.endswith(".paracode"):
                        run = lastRun
                else:
                    run = ""
                if run != "":
                    newText = 'RUN("' + run + '")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
                else:
                    newText = 'RUN("main.para")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
                    newText = 'RUN("main.paracode")'
                    result, error = basic.run('<stdin>', newText)
                    if debug:
                        print(newText)
            elif text.strip().endswith('.para') or text.strip().endswith('.paracode'):
                result, error = basic.run('<stdin>', 'RUN("' + text + '")')
            elif text.startswith('RUN'):
                if text.endswith('.para")') or text.endswith('.paracode")') or text.endswith('.para)') or text.endswith('.paracode)'):
                    result, error = basic.run('<stdin>', text)
                    start = text.find('RUN("') + len('RUN("')
                    end = text.find('")')
                    substring = text[start:end]
                    with open(os.path.realpath(__file__).replace("shell.py", "") + "preferences.toml", "w") as f:
                        f.write('lastRun = "' + substring + '"')
                else:
                    if '("' in text and '")' in text:
                        if "." in text:
                            print(
                                "Unknown file! Make sure the file exists and has either the .para or .paracode file "
                                "extension")
                            Run("")
                        else:
                            newText = text.replace('")', '.para")')
                            result, error = basic.run('<stdin>', newText)
                            if debug:
                                print(newText)
                            newText = text
                            newText = text.replace('")', '.paracode")')
                            result, error = basic.run('<stdin>', newText)
                            if debug:
                                print(newText)
                    else:
                        newText = text.replace('(', '("')
                        newText = newText.replace(')', '")')
                        result, error = basic.run('<stdin>', newText)
                        newText2 = newText
                        if debug:
                            print(newText)
                        if "." in newText:
                            print(
                                "Unknown file! Make sure the file exists and has either the .para or .paracode file "
                                "extension")
                            Run("")
                        else:
                            newText = newText.replace('")', '.para")')
                            result, error = basic.run('<stdin>', newText)
                            if debug:
                                print(newText)
                            newText = newText2
                            newText = newText.replace('")', '.paracode")')
                            result, error = basic.run('<stdin>', newText)
                            if debug:
                                print(newText)
            elif text.startswith("PRINT"):
                result, error = basic.run('<stdin>', text)
            elif text.strip() != "":
                y = text.split(" ")
                c = text.split(" ")[0]
                del (y[0])
                y = ','.join(y)
                sig = ''
                prm = [0, 0]
                try:
                    try:
                        for x in basic.KEYWORDS:
                            if text.startswith(x):
                                result, error = basic.run('<stdin>', text)
                        else:
                            if func(e("config." + c)):
                                sig = sign(e("config." + text.split(" ")[0]))
                                for key in list(dict(sig.parameters).keys()):
                                    if str(dict(sig.parameters)[key]).startswith("{}=".format(key)):
                                        prm[1] += 1
                                    else:
                                        prm[0] += 1
                                if (len(y.split(",")) == prm[0] or y.split(",") == ['']) or len(y.split(",")) <= (
                                        prm[0] + prm[1]):
                                    try:
                                        if not y == "":
                                            e("config." + c + "(" + y + ")")
                                        else:
                                            try:
                                                e("config." + c + "()")
                                            except:
                                                print("<[function] {}>".format(c))
                                    except TypeError:
                                        print(error_color + error_style + errorfx.type_error.format(text))
                                    except NameError:
                                        print(error_color + error_style + errorfx.name_error.format(text))
                                else:
                                    print(error_color + error_style + errorfx.invalid_parameter_error.format(
                                        required_params=prm[0],
                                        optional_params=prm[1],
                                        params_given=len(
                                            y.split(","))))

                            else:
                                raise AttributeError

                    except:
                        if func(e("config." + c)):
                            sig = sign(e("config." + text.split(" ")[0]))
                            for key in list(dict(sig.parameters).keys()):
                                if str(dict(sig.parameters)[key]).startswith("{}=".format(key)):
                                    prm[1] += 1
                                else:
                                    prm[0] += 1
                            if (len(y.split(",")) == prm[0] or y.split(",") == ['']) or len(y.split(",")) <= (
                                    prm[0] + prm[1]):
                                try:
                                    if not y == "":
                                        e("config." + c + "(" + y + ")")
                                    else:
                                        try:
                                            e("config." + c + "()")
                                        except:
                                            print("<[function] {}>".format(c))
                                except TypeError:
                                    print(error_color + error_style + errorfx.type_error.format(text))
                                except NameError:
                                    print(error_color + error_style + errorfx.name_error.format(text))
                            else:
                                print(error_color + error_style + errorfx.invalid_parameter_error.format(
                                    required_params=prm[0],
                                    optional_params=prm[1],
                                    params_given=len(y.split(","))))

                        else:
                            raise AttributeError
                except (AttributeError, SyntaxError):
                    print(error_color + error_style + errorfx.syntax_error.format(text))

            executed = 1
            SetStopped(0)
            RunAgain()
    print("HE")
    return


def RunAgain():
    global executed

    executed = 0
    Run("")


def StartsWith(string, locate):
    return string.lower().startswith(locate.lower())


def CheckExec(sigint, frame):
    ExitExec(stopped)


def ExitExec(stopped2):
    stopped3 = stopped2
    if stopped3 == 0:
        SetCanSubmit(False)
        SetStopped(2)

        sys.stdout = open(os.devnull, 'w')
        if platform.system() == "Windows":
            keyboard = Controller()
            keyboard.press(Key.enter)
        else:
            keyb.press_and_release('enter')
        sys.stdout.close()
        sys.stdout = originalStdout
        print("")

        SetCanSubmit(True)
    elif stopped2 == 2:
        if platform.system() == "Windows":
            shell = win32com.client.Dispatch("WScript.Shell")
            time.sleep(0.5)
            shell.SendKeys('%{F4}')
            sys.stdout = open(os.devnull, 'w')
        elif platform.system() == "Linux":
            keyb.press_and_release('ctrl+q')
            sys.stdout = open(os.devnull, 'w')
        else:
            keyb.press_and_release('cmd+w')
            sys.stdout = open(os.devnull, 'w')


def SetStopped(stopped3):
    global stopped

    stopped = stopped3

    if stopped == 0:
        sys.stdout = originalStdout

def SetCanSubmit(submit):
    global canSubmit

    canSubmit = submit


while True:
    returned = config.returned

    if used == 0:
        # print('ParaCode Shell Launched Successfully!')
        # print("")
        # print("")
        # print("")
        if __name__ == "__main__":
            os.system('')
            init()
            originalSigInt = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, CheckExec)
            args = sys.argv
            if len(args) == 2:
                print(pointer_color + pointer_style + pointer + console_color + console_style + " " + args[1])
                time.sleep(1.25)
                Run(args[1])
            else:
                Run("")
        used = 1

    if canSubmit:
        if keyb.is_pressed('enter'):
            SetStopped(0)

    # else:
    # print("")
    # print(f"Argument {i:>6}: {arg}")
    # if text == "ParaCodeTest.para":

    # if error:
    #    print(error.as_string())
    # elif result:
    #    if len(result.elements) == 1:
    #        print(repr(result.elements[0]))
    #    else:
    #        print(repr(result))
