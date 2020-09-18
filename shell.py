# shell.py

import basic
import config

used = 0
debug = 1

# -- Configuration (Settings) -- #
user_color = "white"
user_style = "white"
console_color = "white"
console_style = "white"

pointer = "\nParaCode Shell >>>"
pointer_color = "green"
pointer_style = "green"


# {} is the command given by the user
class error:
    syntax_error = "Error: '{}' is not a valid command."
    name_error = "Error: '{}' is not defined."
    type_error = "Error: wrong type for '{}'"
    invalid_parameter_error = "Error: {required_params} required parameters required and {optional_params} optional parameters needed but {params_given} given."


class errorfx:
    syntax_error = "Error: '{}' is not a valid command."
    name_error = "Error: '{}' is not defined."
    type_error = "Error: wrong type for '{}'"
    invalid_parameter_error = "Error: {required_params} required parameters required and {optional_params} optional parameters needed but {params_given} given."


error_color = "red"
error_style = "red"

do_help_command = config.do_help_command
help_command = config.help_command

version = config.version
language_name = config.language_name
author = config.author

clear_command = config.clear_command
version_command = config.version_command

# == TO CONFIGURATE THE COMMANDS, GO TO CONFIG.PY == #


# -- Compiler -- #
# this is the compiler, don't touch unless you understand it

from inspect import signature as s, isfunction as f
from json import loads as parse, dumps as stringify
import config

sytling = {
    "white": "\033[0m",
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "purple": "\033[35",
    "cyan": "\033[36m",
    "orange": "\033[33m",
		"bright_black": "\033[90m",
		"bright_red": "\033[91m",
		"bright_green": "\033[92m",
		"bright_yellow": "\033[93m",
		"bright_blue": "\033[94m",
		"bright_magenta": "\033[95m",
		"bright_cyan": "\033[96m",
		"bright_white": "\033[97m",
		"underline": "\033[4m",
		"italic": "\033[3m",
		"darken": "\033[2m",
		"invisible":"\033[08m",
		"reverse":"\033[07m",
		"reset":"\033[0m"
}


def e(c):
    exec('global i; i = %s' % c)
    global i
    return i


try:
    user_color = sytling[user_color]
    user_style = sytling[user_style]
    console_color = sytling[console_color]
    console_style = sytling[console_style]
    pointer_color = sytling[pointer_color]
    pointer_style = sytling[pointer_style]
    error_color = sytling[error_color]
    error_style = sytling[error_style]
except:
    print("\033[31mInvalid colors in configuration.\033[0m")

if do_help_command:
    print("{} {} [{}] 2020 (c)\nType HELP, CREDITS, or LICENSE for more information.".format(language_name, version,
                                                                                             author))
else:
    print("{} {} [{}] 2020 (c)\nType CREDITS, or LICENSE for more information.".format(language_name, version, author))

help = '== Help ==\nFor help with a command, type HELP [command]'


def Run():
    global debug
    global error
    global errorfx
    while True:
        text = input(pointer_color + pointer_style + pointer + console_color + console_style + " ")
        if text.strip() == "": continue
        if debug == 1:
            print(text)
        if text.startswith(help_command + " ") and do_help_command:
            text = text.split(help_command + " ")[1]
            try:
                if f(e("config." + text)):
                    print("== Help | " + text + " ==")
                    h = []
                    prm = [0, 0]
                    co = 0
                    sig = s(e("config." + text.split(" ")[0]))
                    for key in list(dict(sig.parameters).keys()):
                        if str(dict(sig.parameters)[key]).startswith("{}=".format(key)):
                            prm[1] += 1
                        else:
                            prm[0] += 1
                    for i in str(s(e("config." + text)))[1:-1].split(", "):
                        if co <= prm[0]:
                            h.append("[" + i.split("=")[0] + "]")
                        else:
                            h.append("(" + i.split("=")[0] + ")")
                        co += 1
                    print("Usage: " + text + " " + ' '.join(h) + "\nParams: " + " | ".join(
                        str(s(e("config." + text)))[1:-1].split(",")))
            except:
                print(error_color + error_style + error.syntax_error.format(text))
        elif text == help_command:
            print("== Help ==\nFor help with a command, type help [command]")
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
                "Thank you to @ChezCoder for the template, make your own at "
                "https://repl.it/@ChezCoder/Template-Operating-System. Thank you to https://repl.it for hosting this "
                "all.")
        elif text in version_command:
            print("ParaCode", version)
        elif text in clear_command:
            print("\033c", end="", flush=True)
            if do_help_command:
                print("{} {} [{}] 2020 (c)\nType HELP, CREDITS, or LICENSE for more information.".format(language_name,
                                                                                                         version,
                                                                                                         author))
            else:
                print(
                    "{} {} [{}] 2020 (c)\nType CREDITS, or LICENSE for more information.".format(language_name, version,
                                                                                                 author))
        elif text == "DEBUG":
            startDebug = debug
            debug = 1
            newText = 'RUN("index.para")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            newText = 'RUN("index.paracode")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            debug = startDebug
        elif text == "TOGGLEDEBUG":
            if debug == 1:
                debug = 0
                print("DEBUG: FALSE")
            else:
                debug = 1
                print("DEBUG: TRUE")
        elif text == "TESTBUG" or text == "TESTDEBUG" or text == "DEBUGTEST":
            startDebug = debug
            debug = 1
            newText = 'RUN("test.para")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            newText = 'RUN("test.paracode")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            debug = startDebug
        elif text == "TEST":
            newText = 'RUN("test.para")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            newText = 'RUN("test.paracode")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
        elif text == "RUN":
            newText = 'RUN("index.para")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
            newText = 'RUN("index.paracode")'
            result, error = basic.run('<stdin>', newText)
            if debug == 1:
                print(newText)
        elif text.strip().endswith('.para') or text.strip().endswith('.paracode'):
            result, error = basic.run('<stdin>', 'RUN("' + text + '")')
        elif text.startswith('RUN'):
            if text.endswith('.para")') or text.endswith('.paracode")'):
                result, error = basic.run('<stdin>', text)
            else:
                if '("' in text and '")' in text:
                    if "." in text:
                        print(
                            "Unknown file! Make sure the file exists and has either the .para or .paracode file extension")
                        Run()
                    else:
                        newText = text.replace('")', '.para")')
                        result, error = basic.run('<stdin>', newText)
                        if debug == 1:
                            print(newText)
                        newText = text
                        newText = text.replace('")', '.paracode")')
                        result, error = basic.run('<stdin>', newText)
                        if debug == 1:
                            print(newText)
                else:
                    newText = text.replace('(', '("')
                    newText = newText.replace(')', '")')
                    result, error = basic.run('<stdin>', newText)
                    newText2 = newText
                    if debug == 1:
                        print(newText)
                    if "." in newText:
                        print(
                            "Unknown file! Make sure the file exists and has either the .para or .paracode file "
                            "extension")
                        Run()
                    else:
                        newText = newText.replace('")', '.para")')
                        result, error = basic.run('<stdin>', newText)
                        if debug == 1:
                            print(newText)
                        newText = newText2
                        newText = newText.replace('")', '.paracode")')
                        result, error = basic.run('<stdin>', newText)
                        if debug == 1:
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
                    a = 0
                    for x in basic.KEYWORDS:
                        if text.startswith(x):
                            result, error = basic.run('<stdin>', text)
                            a = 1
                    else:
                        if f(e("config." + c)):
                            sig = s(e("config." + text.split(" ")[0]))
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
                                print(error_color + error_style + errorfx.invalid_parameter_error.format(required_params=prm[0],
                                                                                           optional_params=prm[1],
                                                                                           params_given=len(
                                                                                               y.split(","))))

                        else:
                            raise AttributeError

                except:
                    if f(e("config." + c)):
                        sig = s(e("config." + text.split(" ")[0]))
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
                            print(error_color + error_style + errorfx.invalid_parameter_error.format(required_params=prm[0],
                                                                                       optional_params=prm[1],
                                                                                       params_given=len(y.split(","))))

                    else:
                        raise AttributeError
            except (AttributeError, SyntaxError):
                print(error_color + error_style + errorfx.syntax_error.format(text))


def RunAgain():
    Run()


while True:
    if used == 0:
        # print('ParaCode Shell Launched Successfully!')
        # print("")
        # print("")
        # print("")
        used = 1
    # else:
    # print("")
    Run()
    # if text == "ParaCodeTest.para":

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
