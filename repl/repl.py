import platform
import os

from lexer import Lexer, TokenType, LexerToken
from parse.parser import Parser
from parse.node import AstNode, NodeType
from parse.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from interpreter.env.builtins import obj_to_string
from error import InterpreterError
from ast_printer import AstPrinter
from util import LogColor

# when including readline, it switches input() over and allows
# text seeking and other cool things
if platform.system() != 'Windows':
    import readline

import signal


class Repl:
    REPL_FILENAME = '<repl>'

    def __init__(self, paraCode):
        self._walkthrough_messages = self.load_walkthrough_messages()

        color = LogColor.Default
        if paraCode.release_stage == "alpha":
            color = "\033[95m"
        elif paraCode.release_stage == "beta":
            color = "\033[34m"
        elif paraCode.release_stage == "development":
            color = "\033[96m"
        elif paraCode.release_stage == "stable":
            color = "\033[92m"
        self.welcome_message = f"""
            ----- P a r a C o d e -----
                {color + (paraCode.release_stage.upper() + " v" + paraCode.version) + LogColor.Default}
            """

        try:
            from requests import get
            latest_version = get("https://api.github.com/repos/DaRubyMiner360/ParaCode/releases/latest")
            if "tag_name" not in latest_version.json() or latest_version.json()["tag_name"] < paraCode.version:
                # Using unstable and/or development/beta version
                self.welcome_message += LogColor.Warning + """
        You are using a possibly unstable
        version! If something doesn't work
        correctly, that is probably why.""" + LogColor.Default
            elif latest_version.json()["tag_name"] > paraCode.version:
                # Update available
                import datetime
                self.welcome_message += LogColor.Warning + """
        Version {} is available to update
        to! It was released {}.
        Download it from GitHub for new
        features and bug fixes.""".format(latest_version.json()["tag_name"], "on " + datetime.datetime.strptime(latest_version.json()["published_at"], "%Y-%m-%dT%H:%M:%SZ").strftime('%A %b %d, %Y at %X')) + LogColor.Default
        except:
            # Error occured (connection failed, couldn't find any releases, etc.)
            pass
        
        # TODO: Check if the user has used ParaCode before.
        self.welcome_message += """
        

        Welcome to ParaCode Rewrite
        (codenamed Peaches).
        
        Let's get started!
        To learn more about ParaCode,
        type one of the following:

  {}
            """.format('\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), self._walkthrough_messages[key][0]), self._walkthrough_messages)))
        
        
        self.paraCode = paraCode
        self.interpreter = Interpreter(SourceLocation(Repl.REPL_FILENAME))

        print(self.welcome_message)

        self.repl_import_defaults()

        signal.signal(signal.SIGINT, self.at_exit)

    def at_exit(self, signal, frame):
        print('\nExiting...')
        exit(0)

    def repl_import_defaults(self):
        # generate import nodes
        repl_import_nodes = [
            Parser.import_file(Parser, 'std/__core__.para'),
            Parser.import_file(Parser, 'std/__repl__.para')
        ]

        # eval asts
        self.eval_line_ast(repl_import_nodes)

    def loop(self):
        while True:
            self.accept_input()

    def load_walkthrough_content(self, filename):
        file_content = open('./doc/{}'.format(filename)).readlines()

        title = file_content[0:1][0].strip().replace('#', '')
        content = ''.join(file_content[1:]).strip()

        return (title, content)

    def load_walkthrough_messages(self):
        from os import walk, path
        import re

        f = []
        for (dirpath, dirnames, filenames) in walk('./doc'):
            f.extend(filenames)
            break

        walkthrough_messages = {}

        for filename in sorted(f):
            try:
                x = re.search("\d\d_([A-Za-z]*)\.md", filename)
                command_name = x[1]

                walkthrough_messages[command_name] = self.load_walkthrough_content(filename)
            except:
                print("Failed to load documentation file {}".format(filename))

        return walkthrough_messages

    def accept_input(self):
        line = ""

        line = input('>>> ')

        trimmed = line.strip()
        if os.path.isfile(trimmed) and (trimmed.endswith(".para") or trimmed.endswith(".paracode")):
            self.paraCode.eval_file(trimmed)
            
            return
        elif trimmed in self._walkthrough_messages or (trimmed.endswith(".md") and trimmed.replace(".md", "", -1) in self._walkthrough_messages) or (trimmed.endswith(".md/") and trimmed.replace(".md/", "", -1) in self._walkthrough_messages):
            print(
                self._walkthrough_messages[trimmed][1].replace('```\n', '').replace('```javascript\n', '').replace('```js\n', '').replace('`', ''))

            return
        elif trimmed == "doc" or trimmed == "docs" or trimmed == "documentation" or trimmed == "documentations" or trimmed == "walkthrough" or trimmed == "walkthroughs":
            print("""
  {}""".format('\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), self._walkthrough_messages[key][0]), self._walkthrough_messages))))
            return

        (brace_counter, bracket_counter, paren_counter, comment_type) = self.count_continuation_tokens(line)

        while brace_counter > 0 or bracket_counter > 0 or paren_counter > 0 or comment_type:
            next_line = input('... ')
            line += next_line + '\n'
            (brace_counter, bracket_counter, paren_counter, comment_type) = self.count_continuation_tokens(line)

        (line_ast, error_list) = self.parse_line(line)

        # for node in line_ast:
        #     AstPrinter().print_ast(node)

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return

        self.eval_line_ast(line_ast)

    def eval_line_ast(self, line_ast):
        last_value = None
        last_node = None

        for node in line_ast:
            last_node = node
            try:
                last_value = self.interpreter.visit(node)
            except InterpreterError:
                self.interpreter.error_list.clear_errors()
                continue

        if last_value is not None:
            obj_str = obj_to_string(self.interpreter, last_node, last_value)
            print(f"{LogColor.Info}{obj_str}{LogColor.Default}")

    def parse_line(self, line):
        lexer = Lexer(line, SourceLocation(Repl.REPL_FILENAME))
        tokens = lexer.lex()

        parser = Parser(tokens, lexer.source_location)

        return (parser.parse(), parser.error_list)

    def count_continuation_tokens(self, line):
        brace_counter = 0
        bracket_counter = 0
        paren_counter = 0

        started_comment_char = ""
        comment_type = ""

        for ch in line:
            if ch == '/' and comment_type == "":
                if started_comment_char != "/":
                    started_comment_char = "/"
                else:
                    started_comment_char = ""
                    comment_type = "slash_slash"
            elif ch == '*' and started_comment_char == "/":
                started_comment_char = ""
                comment_type = "slash_asterisk"
            elif ch == '#' and comment_type == "" and started_comment_char != "#":
                started_comment_char = "#"
                comment_type = "hashtag"
            elif ch == '*' and started_comment_char == "#":
                started_comment_char = ""
                comment_type = "hashtag_asterisk"
            elif ch == '*' and started_comment_char == "":
                started_comment_char = "*"
            elif ch == '/' and started_comment_char == "*" and comment_type == "slash_asterisk":
                started_comment_char = ""
                comment_type = ""
            elif ch == '#' and started_comment_char == "*" and comment_type == "hashtag_asterisk":
                started_comment_char = ""
                comment_type = ""

            elif ch == '{' and comment_type == "":
                brace_counter += 1
            elif ch == '}' and comment_type == "":
                brace_counter -= 1
            elif ch == '(' and comment_type == "":
                paren_counter += 1
            elif ch == ')' and comment_type == "":
                paren_counter -= 1
            elif ch == '[' and comment_type == "":
                bracket_counter += 1
            elif ch == ']' and comment_type == "":
                bracket_counter -= 1

        if comment_type == "slash_slash" or comment_type == "hashtag":
            comment_type = ""

        return (brace_counter, bracket_counter, paren_counter, comment_type)
