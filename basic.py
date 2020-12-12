#######################################
# IMPORTS
#######################################

from strings_with_arrows import *

from colorama import Fore as coloramaFore
from colorama import Back as coloramaBack
from colorama import Style as coloramaStyle
from colorama import init
from colored import fore as Fore
from colored import back as Back
from colored import fg as Fg
from colored import bg as Bg
from colored import style as Style

import sys
import os

import importlib

import random
from cryptography.fernet import Fernet
import base64

import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS

import string
import math
from datetime import date
from datetime import time
import datetime

import tkinter as tk
import turtle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import discord
from dotenv import load_dotenv

# pip install Kivy
# import Kivy
# import PyQT

#######################################
# STYLING
#######################################
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

# importing = True
originalStdout = sys.stdout
value = "main.para"

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# TOKENS
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_EQ = 'EQ'
TT_MODULO = 'MODULO'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_ARROW = 'ARROW'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'

KEYWORDS = [
    'VAR',
    'VARIABLE',
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELIF',
    'ELSE',
    'FOR',
    'TO',
    'STEP',
    'WHILE',
    'FUNCTION',
    'FUNC',
    'THEN',
    'END',
    'RETURN',
    'CONTINUE',
    'BREAK',
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.text[self.pos.idx:self.pos.idx + 2] == "//":
                self.skip_comment()
            elif self.current_char == ';':
                self.skip_comment()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char in '\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == "'":
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MODULO, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
            escape_character = False

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.advance()

        while self.current_char != '\n':
            self.advance()

        self.advance()


#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end


class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end


class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end


class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))
        return res

    ###################################

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'RETURN'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'CONTINUE'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'BREAK'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'VARIABLE', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR') or self.current_tok.matches(TT_KEYWORD, 'VARIABLE'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'VAR', 'VARIABLE', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC' or 'NOT'"
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'VAR', 'VARIABLE', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'FUNCTION'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        elif tok.matches(TT_KEYWORD, 'FUNC'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC'"
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'VAR', 'VARIABLE', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('IF'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('ELIF')

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'END'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'END'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, 'END'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FUNCTION') and not self.current_tok.matches(TT_KEYWORD, 'FUNC'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FUNCTION' or 'FUNC'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'END'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)


#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        # Note: this will allow you to continue and break outside the current function
        return (
                self.error or
                self.func_return_value or
                self.loop_should_continue or
                self.loop_should_break
        )


#######################################
# VALUES
#######################################

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modulo_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def index_of(self, other):
        result = self.elements[other]
        return result, None

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class OptionalBaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args, required_arg_names):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(required_arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(required_arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx, required_arg_names):
        res = RTResult()
        res.register(self.check_args(arg_names, args, required_arg_names))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class OptionalFunction(OptionalBaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx, method.required_arg_names))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = OptionalFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    #####################################

    client = discord.Client()
    token = os.environ["TOKEN"]

    def execute_print(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        color = str(exec_ctx.symbol_table.get('color')).lower()
        if value is not None:
            if color is not None:
                if color.startswith('#'):
                    print(Fg(color) + value + sytling.get("reset"))
                elif color in sytling:
                    print(sytling.get(color) + value + sytling.get("reset"))
                elif exec_ctx.symbol_table.get('color') in sytling:
                    print(sytling.get(str(exec_ctx.symbol_table.get('color'))) + value + sytling.get("reset"))
                else:
                    print(value)
            else:
                print(value)
        else:
            print()
        return RTResult().success(Number.null)

    execute_print.arg_names = ['value', 'color']
    execute_print.required_arg_names = []

    def execute_discordclient(self, exec_ctx):
        self.client = discord.Client()
        return RTResult().success(Number(self.client))

    execute_discordclient.arg_names = []
    execute_discordclient.required_arg_names = []

    def execute_discordtoken(self, exec_ctx):
        if exec_ctx.symbol_table.get('token') is not None:
            self.token = str(exec_ctx.symbol_table.get('token'))
        else:
            return RTResult().success(Number(self.token))
        return RTResult().success(Number.null)

    execute_discordtoken.arg_names = ['token']
    execute_discordtoken.required_arg_names = []

    joinmessage = 'Bot Online!'

    def execute_ondiscordbotready(self, exec_ctx):
        self.joinmessage = str(exec_ctx.symbol_table.get('message'))
        return RTResult().success(Number.null)

    execute_ondiscordbotready.arg_names = ['message']
    execute_ondiscordbotready.required_arg_names = ['message']

    @client.event
    async def on_ready():
        print(OptionalFunction.joinmessage)

    action = "PRINT(\"Hello, World!\")"
    messageAuthor = None
    messageAuthorName = ""
    messageContent = ""
    message = None
    messageChannel = None

    def execute_ondiscordbotmessage(self, exec_ctx):
        if exec_ctx.symbol_table.get('action') is not None:
            self.action = str(exec_ctx.symbol_table.get('action'))
        return RTResult().success(Number.null)

    execute_ondiscordbotmessage.arg_names = ['action']
    execute_ondiscordbotmessage.required_arg_names = []

    @client.event
    async def on_message(message):
        OptionalFunction.messageAuthor = message.author
        OptionalFunction.messageAuthorName = message.author.name
        OptionalFunction.messageContent = message.content
        OptionalFunction.message = message
        OptionalFunction.messageChannel = message.channel
        if OptionalFunction.action is not None:
            run('<stdin>', OptionalFunction.action.replace("${messageAuthor}", messageAuthor).replace("${messageauthor}", messageAuthor).replace("${messageAuthorName}", messageAuthorName).replace("${messageauthorname}", messageAuthorName).replace("${messageContent}", messageContent).replace("${messagecontent}", messageContent).replace("${message}", message).replace("${messageChannel}", messageChannel).replace("${messagechannel}", messageChannel))

    def execute_discordbotsendmessage(self, exec_ctx):
        message = str(exec_ctx.symbol_table.get('message'))
        channel = self.message.channel
        channel.send(message)
        return RTResult().success(Number.null)

    execute_discordbotsendmessage.arg_names = ['message']
    execute_discordbotsendmessage.required_arg_names = ['message']

    def execute_rundiscordbot(self, exec_ctx):
        token = self.token
        if exec_ctx.symbol_table.get('token') is not None:
            token = str(exec_ctx.symbol_table.get('token'))
        self.client.run(token)
        return RTResult().success(Number.null)

    execute_rundiscordbot.arg_names = ['token']
    execute_rundiscordbot.required_arg_names = []

    # def execute_Import(self, exec_ctx):
    #     global value

    #     value2 = str(exec_ctx.symbol_table.get('file'))
    #     file = None
    #     code = ""
    #     code2 = ""
    #     if os.path.exists(value):
    #         file = open(value,"r")
    #         code = file.readlines()
    #     else:
    #         if os.path.exists('temp.core.para'):
    #             file = open("temp.core.para","r")
    #             code = file.readlines()
    #             code2 = value
    #         else:
    #             file = open("temp.core.para", "w+")
    #             # print(value)
    #             file.write(value)
    #             file.close()
    #             file = open("temp.core.para","r")
    #             code = file.readlines()
    #     resultCode = code
    #     result = value
    #     b = open(value2,"r").read()
    #     print(value2)
    #     for i in resultCode:
    #         a = True
    #         for o in range(len(resultCode)):
    #             if i.startswith(f'IMPORT("{value2}")') or resultCode[o].startswith(f'IMPORT("{value2}")'):
    #                 a = False
    #                 resultCode[o - 1] = ""
    #                 resultCode[o] = b + "\n"
    #                 #result += ""
    #             else:
    #                 a = True
    #         if a:
    #             result += i
    #     sys.stdout = originalStdout
    #     print(result)
    #     value = result
    #     run('<stdin>', result)
    #     if not "IMPORT" in result:
    #         if os.path.exists("temp.core.para"):
    #             os.remove("temp.core.para")
    #     return RTResult().success(String(result))

    # execute_Import.arg_names = ['file']
    # execute_Import.required_arg_names = ['file']

    

    def execute_input(self, exec_ctx):
        inputText = str(exec_ctx.symbol_table.get('inputText'))
        if inputText is None or inputText == "":
            text = input()
        else:
            text = input(inputText)
        return RTResult().success(String(text))

    execute_input.arg_names = ['inputText']
    execute_input.required_arg_names = []

    def execute_paragameinit(self, exec_ctx):
        pygame.init()
        if exec_ctx.symbol_table.get('width') is not None and exec_ctx.symbol_table.get('height') is not None:
            gameDisplay = pygame.display.set_mode(
                (int(str(exec_ctx.symbol_table.get('width'))), int(str(exec_ctx.symbol_table.get('height')))))
        else:
            gameDisplay = pygame.display.set_mode((800, 600))

        if exec_ctx.symbol_table.get('caption') is not None:
            pygame.display.set_caption(str(exec_ctx.symbol_table.get('caption')))
        return RTResult().success(Number(gameDisplay))

    execute_paragameinit.arg_names = ['width', 'height', 'caption']
    execute_paragameinit.required_arg_names = []

    def execute_randomnumber(self, exec_ctx):
        beg = int(str(exec_ctx.symbol_table.get('beg')))
        end = int(str(exec_ctx.symbol_table.get('end')))
        step = int(str(exec_ctx.symbol_table.get('step')))
        if beg is not None:
            if end is not None:
                if step is not None:
                    value = random.randrange(beg, end, step)
        else:
            value = random.random()
        return RTResult().success(Number(value))

    execute_randomnumber.arg_names = ['beg', 'end', 'step']
    execute_randomnumber.required_arg_names = []

    def execute_label(self, exec_ctx):
        # else:
            # label = tk.Label(text=str(exec_ctx.symbol_table.get('text')))
            # label.pack()
        label = tk.Label(text=str(exec_ctx.symbol_table.get('text')))
        label.pack()
        return RTResult().success(Number(label))

    execute_label.arg_names = ['text', 'background', 'foreground', 'width', 'height']
    execute_label.required_arg_names = ['text']

    def execute_button(self, exec_ctx):
        # else:
            # label = tk.Label(text=str(exec_ctx.symbol_table.get('text')))
            # label.pack()
        button = tk.Button(text=str(exec_ctx.symbol_table.get('text')))
        button.pack()
        return RTResult().success(Number(button))

    execute_button.arg_names = ['text', 'bg', 'fg', 'width', 'height']
    execute_button.required_arg_names = ['text']

    def execute_entry(self, exec_ctx):
        # else:
            # label = tk.Label(text=str(exec_ctx.symbol_table.get('text')))
            # label.pack()
        entry = tk.Entry(text=str(exec_ctx.symbol_table.get('text')))
        entry.pack()
        return RTResult().success(Number(entry))

    execute_entry.arg_names = ['bg', 'fg', 'width', 'height']
    execute_entry.required_arg_names = []

    def execute_parabuild(self, exec_ctx):
        from shutil import copyfile
        if str(exec_ctx.symbol_table.get('file')).endswith('.para') or str(exec_ctx.symbol_table.get('file')).endswith('.paracode'):
            if exec_ctx.symbol_table.get('name') is not None and int(str(exec_ctx.symbol_table.get('name'))) != 0:
                copyfile('shellTemplate.py', str(exec_ctx.symbol_table.get('name')) + ".py")
                file = open(str(exec_ctx.symbol_table.get('name') + ".py"), 'r')
                contents = file.read()
                file.close()
                file = open(str(exec_ctx.symbol_table.get('name') + ".py"), 'w')
                file.write(contents.replace('shellTemplate.para', str(exec_ctx.symbol_table.get('file'))))

                if exec_ctx.symbol_table.get('icon') is not None:
                    os.system('pyinstaller --onefile --add-data="' + str(exec_ctx.symbol_table.get('file')) + '"' + str(exec_ctx.symbol_table.get('file')).replace('.para', '.py') + ' --icon=' + str(exec_ctx.symbol_table.get('icon')) + ' --name=' + str(exec_ctx.symbol_table.get('name')))
                else:
                    os.system('pyinstaller --onefile --add-data="' + str(exec_ctx.symbol_table.get('file')) + '"' + str(exec_ctx.symbol_table.get('file')).replace('.para', '.py') + ' --name=' + str(exec_ctx.symbol_table.get('name')))

                os.path.remove(str(exec_ctx.symbol_table.get('name')).replace('.para', '.py'))
            else:
                copyfile('shellTemplate.py', str(exec_ctx.symbol_table.get('file')).replace('.para', '.py'))
                file = open(str(exec_ctx.symbol_table.get('file')).replace('.para', '.py'), 'r')
                contents = file.read()
                file.close()
                file = open(str(exec_ctx.symbol_table.get('file')).replace('.para', '.py'), 'w')
                file.write(contents.replace('shellTemplate.para', str(exec_ctx.symbol_table.get('file'))))

                if exec_ctx.symbol_table.get('icon') is not None:
                    os.system('pyinstaller --onefile --add-data="' + str(exec_ctx.symbol_table.get('file')) + '"' + str(exec_ctx.symbol_table.get('file')).replace('.para', '.py') + ' --icon=' + str(exec_ctx.symbol_table.get('icon')))
                else:
                    os.system('pyinstaller --onefile --add-data="' + str(exec_ctx.symbol_table.get('file')) + '"' + str(exec_ctx.symbol_table.get('file')).replace('.para', '.py'))

                os.path.remove(str(exec_ctx.symbol_table.get('file')).replace('.para', '.py'))

        return RTResult().success(Number.null)

    execute_parabuild.arg_names = ['file', 'name', 'icon']
    execute_parabuild.required_arg_names = ['file']


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"


class BuiltInFunction(BaseFunction):
    builtInWindow = None

    builtInTurtle = None
    builtInTurtleScreen = None
    builtInTurtlePen = None

    builtInRecognizer = None
    builtInMicrophone = None
    builtInTranslator = None

    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    #####################################

    def execute_printColor(self, exec_ctx):
        if str(exec_ctx.symbol_table.get('color')).startswith('#'):
            print(str(exec_ctx.symbol_table.get('color')), str(
                exec_ctx.symbol_table.get('value')), sytling.get("reset"))
        if str(exec_ctx.symbol_table.get('color')).lower() in sytling:
            print(sytling.get(str(exec_ctx.symbol_table.get('color')).lower()) + str(
                exec_ctx.symbol_table.get('value')) + sytling.get("reset"))
        elif exec_ctx.symbol_table.get('color') in sytling:
            print(sytling.get(str(exec_ctx.symbol_table.get('color')).lower()) + str(
                exec_ctx.symbol_table.get('value')) + sytling.get("reset"))
        else:
            print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_printColor.arg_names = ['value', 'color']

    def execute_recognizer(self, exec_ctx):
        recog = spr.Recognizer()
        builtInRecognizer = recog
        return RTResult().success(Number(recog))

    execute_recognizer.arg_names = []

    def execute_microphone(self, exec_ctx):
        mc = spr.Microphone()
        builtInMicrophone = mc
        return RTResult().success(Number(mc))

    execute_microphone.arg_names = []

    def execute_translator(self, exec_ctx):
        translator = Translator()
        self.builtInTranslator = translator
        return RTResult().success(Number(translator))

    execute_translator.arg_names = []

    def execute_translate(self, exec_ctx):
        # translator = self.builtInTranslator
        translator = Translator()
        value = str(exec_ctx.symbol_table.get('value'))
        fromLang = str(exec_ctx.symbol_table.get('fromLang'))
        toLang = str(exec_ctx.symbol_table.get('toLang'))
        result = translator.translate(value, src= fromLang, dest= toLang).text
        return RTResult().success(Number(result))

    execute_translate.arg_names = ['value', 'fromLang', 'toLang']

    def execute_modulo(self, exec_ctx):
        a = int(str(exec_ctx.symbol_table.get('valueOne')))
        b = int(str(exec_ctx.symbol_table.get('valueTwo')))
        c = a % b
        return RTResult().success(Number(c))

    execute_modulo.arg_names = ['valueOne', 'valueTwo']

    def execute_indexof(self, exec_ctx):
        a = exec_ctx.symbol_table.get('list')
        b = int(str(exec_ctx.symbol_table.get('index')))
        c = a.index_of(b)
        return RTResult().success(
            Number(str(c).replace('"', '').replace(', ', '').replace('None', '').replace('(', '').replace(')', '')))

    execute_indexof.arg_names = ['list', 'index']

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))

    execute_print_ret.arg_names = ['value']

    def execute_cryptogeneratekey(self, exec_ctx):
        key = Fernet.generate_key()
        return RTResult().success(Number(key))

    execute_cryptogeneratekey.arg_names = []

    def execute_cryptoencrypt(self, exec_ctx):
        key = str(exec_ctx.symbol_table.get('key'))
        value = str(exec_ctx.symbol_table.get('value'))
        encryptionType = Fernet(key)
        encryptedMessage = encryptionType.encrypt(value)
        encryptedMessage = encryptedMessage.decode("ascii")
        return RTResult().success(Number(encryptedMessage))

    execute_cryptoencrypt.arg_names = ['key', 'value']
    
    def execute_cryptodecrypt(self, exec_ctx):
        key = str(exec_ctx.symbol_table.get('key'))
        encryptedMessage = str(exec_ctx.symbol_table.get('encryptedMessage'))
        encryptionType = Fernet(key)
        decryptedMessage = encryptionType.decrypt(encryptedMessage)
        return RTResult().success(Number(decryptedMessage))

    execute_cryptodecrypt.arg_names = ['key', 'encryptedMessage']

    def execute_cryptoencode(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        message_bytes = value.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        encodedMessage = base64_bytes.decode("ascii")

        return RTResult().success(Number(encodedMessage))

    execute_cryptoencode.arg_names = ['value']
    
    def execute_cryptodecode(self, exec_ctx):
        encodedMessage = str(exec_ctx.symbol_table.get('encodedMessage'))
        base64_bytes = encodedMessage.encode("ascii") 
        message_bytes = base64.b64decode(base64_bytes)
        decodedMessage = message_bytes.decode('ascii')

        return RTResult().success(Number(decodedMessage))

    execute_cryptodecode.arg_names = ['encodedMessage']

    def execute_oslogout(self, exec_ctx):
        os.system("shutdown -1")
        return RTResult().success(Number.null)

    execute_oslogout.arg_names = []

    def execute_osrestart(self, exec_ctx):
        os.system("shutdown /r /t 1")
        return RTResult().success(Number.null)

    execute_osrestart.arg_names = []

    def execute_osshutdown(self, exec_ctx):
        os.system("shutdown /s /t 1")
        return RTResult().success(Number.null)

    execute_osshutdown.arg_names = []

    def execute_ossys(self, exec_ctx):
        os.system(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_ossys.arg_names = ['value']

    def execute_app(self, exec_ctx):
        window = tk.Tk()
        BuiltInFunction.builtInWindow = window
        return RTResult().success(Number(window))

    execute_app.arg_names = []

    def execute_tk(self, exec_ctx):
        window = tk.Tk()
        BuiltInFunction.builtInWindow = window
        return RTResult().success(Number(window))

    execute_tk.arg_names = []

    def execute_coloredlabel(self, exec_ctx):
        label = tk.Label(text=str(exec_ctx.symbol_table.get('text')),
                         foreground=str(exec_ctx.symbol_table.get('foreground')).lower(),
                         background=str(exec_ctx.symbol_table.get('background')).lower())
        label.pack()
        return RTResult().success(Number(label))

    execute_coloredlabel.arg_names = ['text', 'background', 'foreground']

    def execute_mainloop(self, exec_ctx):
        window = BuiltInFunction.builtInWindow
        window.mainloop()
        return RTResult().success(Number(window))

    execute_mainloop.arg_names = []

    def execute_mainloopapp(self, exec_ctx):
        window = tk.Tk()
        window.mainloop()
        BuiltInFunction.builtInWindow = window
        return RTResult().success(Number(window))

    execute_mainloopapp.arg_names = []

    def execute_demoapp(self, exec_ctx):
        enable = str(exec_ctx.symbol_table.get('enable'))
        print("HELLOG")
        if enable == "TRUE":
            print("HELLOG")
            window = tk.Tk()
            window.mainloop()
            print("HELLOG")
            hello = tk.Label(text="HELLO, WORLD!")
            hello.pack()
            label = tk.Label(text="FROM PARACODE!")
            label.pack()
            return RTResult().success(Number(window))
        return RTResult().success(Number.null)

    execute_demoapp.arg_names = ['enable']

    def execute_stairs(self, exec_ctx):
        N = int(str(exec_ctx.symbol_table.get('count')))
        i = 1
        while i < steps:
            print('  '*i+'|_')
            i = i + 1
        print('__'*i+'|')
        return RTResult().success(Number.null)

    execute_stairs.arg_names = ['count']
    
    def execute_halfDiamondStar(self, exec_ctx):
        N = int(str(exec_ctx.symbol_table.get('count')))
        for i in range(N):
            for j in range(0, i + 1):
                print("*", end="")
            print()

        for i in range(1, N):
            for j in range(i, N):
                print("*", end="")
            print()
        return RTResult().success(Number.null)

    execute_halfDiamondStar.arg_names = ['count']

    def execute_removepunc(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        punctuation = string.punctuation
        for ele in value:
            if ele in punctuation:
                value = value.replace(ele, "")
        return RTResult().success(Number(value))

    execute_removepunc.arg_names = ['value']

    def execute_removeallspaces(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        punctuation = '''_ '''
        for ele in value:
            if ele in punctuation:
                value = value.replace(ele, "")
        return RTResult().success(Number(value))

    execute_removeallspaces.arg_names = ['value']

    def execute_removespaces(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        value = value.replace(" ", "")
        return RTResult().success(Number(value))

    execute_removespaces.arg_names = ['value']

    def execute_removeletters(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        letters = LETTERS
        for ele in value:
            if ele in letters:
                value = value.replace(ele, "")
        return RTResult().success(Number(value))

    execute_removeletters.arg_names = ['value']

    def execute_removenumbers(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        numbers = DIGITS
        for ele in value:
            if ele in numbers:
                value = value.replace(ele, "")
        return RTResult().success(Number(value))

    execute_removenumbers.arg_names = ['value']

    def execute_keeppunc(self, exec_ctx):
        value = str(exec_ctx.symbol_table.get('value'))
        punctuation = string.punctuation
        for ele in value:
            if ele not in punctuation:
                value = value.replace(ele, "")
        return RTResult().success(Number(value))

    execute_keeppunc.arg_names = ['value']

    def execute_turtle(self, exec_ctx):
        t = turtle.Turtle()
        turtle.title("ParaCode Turtle Graphics")
        BuiltInFunction.builtInTurtle = t
        return RTResult().success(Number(t))

    execute_turtle.arg_names = []

    def execute_turtlescreen(self, exec_ctx):
        s = turtle.getscreen()
        s.title("ParaCode Turtle Graphics")
        BuiltInFunction.builtInTurtleScreen = s
        return RTResult().success(Number(s))

    execute_turtlescreen.arg_names = []

    def execute_turtleright(self, exec_ctx):
        turtle.right(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtleright.arg_names = ['value']

    def execute_turtleleft(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.left(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtleleft.arg_names = ['value']

    def execute_turtleup(self, exec_ctx):
        turtle.up()
        return RTResult().success(Number.null)

    execute_turtleup.arg_names = []

    def execute_turtledown(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.down()
        return RTResult().success(Number.null)

    execute_turtledown.arg_names = []

    def execute_turtlehide(self, exec_ctx):
        turtle.hideturtle()
        return RTResult().success(Number.null)

    execute_turtlehide.arg_names = []

    def execute_turtlependown(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.pendown()
        return RTResult().success(Number.null)

    execute_turtlependown.arg_names = []

    def execute_turtlewidth(self, exec_ctx):
        turtle.width(width=int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtlewidth.arg_names = ['value']

    def execute_turtlecircle(self, exec_ctx):
        turtle.circle(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtlecircle.arg_names = ['value']

    def execute_turtlespeed(self, exec_ctx):
        turtle.speed(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtlespeed.arg_names = ['value']

    def execute_turtlepenup(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.penup()
        return RTResult().success(Number.null)

    execute_turtlepenup.arg_names = []

    def execute_turtlebackward(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.backward(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtlebackward.arg_names = ['value']

    def execute_turtleforward(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.forward(int(str(exec_ctx.symbol_table.get('value'))))
        return RTResult().success(Number.null)

    execute_turtleforward.arg_names = ['value']

    def execute_turtletitle(self, exec_ctx):
        turtle.title(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_turtletitle.arg_names = ['value']

    def execute_turtlecolor(self, exec_ctx):
        turtle.color(str(exec_ctx.symbol_table.get('color')))
        return RTResult().success(Number.null)

    execute_turtlecolor.arg_names = ['color']

    def execute_turtlefillcolor(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.fillcolor(str(exec_ctx.symbol_table.get('color')))
        return RTResult().success(Number.null)

    execute_turtlefillcolor.arg_names = ['color']

    def execute_turtleheading(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.heading(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_turtleheading.arg_names = ['value']

    def execute_turtleposition(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        return RTResult().success(Number(t.position()))

    execute_turtleposition.arg_names = []

    def execute_turtlebgcolor(self, exec_ctx):
        t = BuiltInFunction.builtInTurtleScreen
        if t is None:
            turtle.bgcolor(str(exec_ctx.symbol_table.get('color')))
            return RTResult().success(Number.null)
        else:
            t.bgcolor(str(exec_ctx.symbol_table.get('color')))
            return RTResult().success(Number.null)

    execute_turtlebgcolor.arg_names = ['color']

    def execute_turtlepencolor(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.pencolor(str(exec_ctx.symbol_table.get('color')))
        return RTResult().success(Number.null)

    execute_turtlepencolor.arg_names = ['color']

    def execute_turtleexitonclick(self, exec_ctx):
        t = BuiltInFunction.builtInTurtle
        t.exitonclick()
        return RTResult().success(Number.null)

    execute_turtleexitonclick.arg_names = []

    def execute_turtlepen(self, exec_ctx):
        p = turtle.pen()
        BuiltInFunction.builtInTurtlePen = p
        return RTResult().success(Number(p))

    execute_turtlepen.arg_names = []

    def execute_openfile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('filename')))
        return RTResult().success(Number(f))

    execute_openfile.arg_names = ['filename']

    def execute_closefile(self, exec_ctx):
        exec_ctx.symbol_table.get('file').close()
        return RTResult().success(Number.null)

    execute_closefile.arg_names = ['file']

    def execute_openfilemode(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('filename')),
                 str(exec_ctx.symbol_table.get('mode')).lower())
        return RTResult().success(Number(f))

    execute_openfilemode.arg_names = ['filename', 'mode']

    def execute_readfile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('file')), "r")
        string = f.read()
        f.close()
        return RTResult().success(Number(string))

    execute_readfile.arg_names = ['file']

    def execute_readpartfile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('file')), "r")
        string = f.read(exec_ctx.symbol_table.get('chars'))
        f.close()
        return RTResult().success(Number(string))

    execute_readpartfile.arg_names = ['file', 'chars']

    def execute_readfileline(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('file')), "r")
        string = f.readline()
        f.close()
        return RTResult().success(Number(string))

    execute_readfileline.arg_names = ['file']

    def execute_writefile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('file')), "w")
        string = f.write(str(exec_ctx.symbol_table.get('string')))
        f.close()
        return RTResult().success(Number(string))

    execute_writefile.arg_names = ['file', 'string']

    def execute_appendfile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('file')), "a")
        string = f.write(str(exec_ctx.symbol_table.get('string')))
        f.close()
        return RTResult().success(Number(string))

    execute_appendfile.arg_names = ['file', 'string']

    def execute_createfile(self, exec_ctx):
        f = open(os.path.realpath(__file__).replace("basic.py", "") + str(exec_ctx.symbol_table.get('filename')), "x")
        f.close()
        return RTResult().success(Number(f))

    execute_createfile.arg_names = ['filename']

    def execute_deletefile(self, exec_ctx):
        os.remove(str(exec_ctx.symbol_table.get('filename')))
        return RTResult().success(Number.null)

    execute_deletefile.arg_names = ['filename']

    def execute_fileexists(self, exec_ctx):
        os.remove()
        return RTResult().success(Number(os.path.exists(str(exec_ctx.symbol_table.get('filename')))))

    execute_fileexists.arg_names = ['filename']

    def execute_deletedirectory(self, exec_ctx):
        os.rmdir(str(exec_ctx.symbol_table.get('directory')))
        return RTResult().success(Number.null)

    execute_deletedirectory.arg_names = ['directory']

    # def execute_join(self, exec_ctx):
    #     elements = str(exec_ctx.symbol_table.get('elements'))
    #     separator = str(exec_ctx.symbol_table.get('separator'))
    #     result = ""
    #     # legn = len(elements)
    #
    #     # for i in range(legn):
    #     # if i != legn:
    #     #     result = result.join(elements) + separator
    #     # else:
    #     #     result = result.join(elements)
    #     result = result + elements + separator
    #
    #     return RTResult().success(Number(result))
    #
    # execute_join.arg_names = ['elements', 'separator']

    def execute_debuglog(self, exec_ctx):
        print("\033[37m" + "Info: " + str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    execute_debuglog.arg_names = ['value']

    def execute_debugwarning(self, exec_ctx):
        print("\033[33m" + ("Warning: " + str(exec_ctx.symbol_table.get('value')) + "\033[37m"))
        return RTResult().success(Number.null)

    execute_debugwarning.arg_names = ['value']

    def execute_debugerror(self, exec_ctx):
        print("\033[91m" + ("Error: " + str(exec_ctx.symbol_table.get('value')) + "\033[37m"))
        return RTResult().success(Number.null)

    execute_debugerror.arg_names = ['value']

    def execute_debugwarn(self, exec_ctx):
        print("\033[33m" + ("Warning: " + str(exec_ctx.symbol_table.get('value')) + "\033[37m"))
        return RTResult().success(Number.null)

    execute_debugwarn.arg_names = ['value']

    def execute_debugerr(self, exec_ctx):
        print("\033[91m" + ("Error: " + str(exec_ctx.symbol_table.get('value')) + "\033[37m"))
        return RTResult().success(Number.null)

    execute_debugerr.arg_names = ['value']

    def execute_debugfatal(self, exec_ctx):
        print("\033[31m" + ("FatalError: " + str(exec_ctx.symbol_table.get('value')) + "\033[37m"))
        return RTResult().success(Number.null)

    execute_debugfatal.arg_names = ['value']

    def execute_gettime(self, exec_ctx):
        return RTResult().success(Number(time.localtime()))

    execute_gettime.arg_names = []

    def execute_getsecond(self, exec_ctx):
        return RTResult().success(Number(time.localtime().second))

    execute_getsecond.arg_names = []

    def execute_getminute(self, exec_ctx):
        return RTResult().success(Number(time.localtime().minute))

    execute_getminute.arg_names = []

    def execute_gethour(self, exec_ctx):
        return RTResult().success(Number(time.localtime().hour))

    execute_gethour.arg_names = []

    def execute_getdate(self, exec_ctx):
        return RTResult().success(Number(date.today()))

    execute_getdate.arg_names = []

    def execute_getdatetime(self, exec_ctx):
        return RTResult().success(Number(datetime.datetime.now()))

    execute_getdatetime.arg_names = []

    def execute_getday(self, exec_ctx):
        return RTResult().success(Number(datetime.datetime.now().day))

    execute_getday.arg_names = []

    def execute_getmonth(self, exec_ctx):
        return RTResult().success(Number(datetime.datetime.now().month))

    execute_getmonth.arg_names = []

    def execute_getyear(self, exec_ctx):
        return RTResult().success(Number(datetime.datetime.now().year))

    execute_getyear.arg_names = []

    def execute_replace(self, exec_ctx):
        string = str(exec_ctx.symbol_table.get('string'))
        string = string.replace(str(exec_ctx.symbol_table.get('value')), str(exec_ctx.symbol_table.get('newValue')))
        return RTResult().success(Number(string))

    execute_replace.arg_names = ['string', 'value', 'newValue']

    def execute_replacefirst(self, exec_ctx):
        string = str(exec_ctx.symbol_table.get('string'))
        string = string.replace(str(exec_ctx.symbol_table.get('value')), str(exec_ctx.symbol_table.get('newValue')), 1)
        return RTResult().success(Number(string))

    execute_replacefirst.arg_names = ['string', 'value', 'newValue']

    def execute_loop(self, exec_ctx):
        # func = getattr("", str(exec_ctx.symbol_table.get('function')))
        for i in range(exec_ctx.symbol_table.get('count')):
            # func
            globals()[exec_ctx.symbol_table.get('function')]
        return RTResult().success(Number.null)

    execute_loop.arg_names = ["function", "count"]

    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls')
        return RTResult().success(Number.null)

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction or OptionalBaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)

    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                #script = 'IMPORT("ParaCore.para")\n\n' + f.read()
                code = ""
                code2 = ""
                code3 = ""
                codelines = []
                file = ""
                imported = []
                isImported = False
                code0 = f.read()
                codelines = code0.splitlines()
                code = code0
                # while any("IMPORT " in s for s in codelines):
                for line in codelines:
                  if line.replace("	", "").replace(" ", "").startswith("#"):
                    code = code.replace(line, "")
                  elif 'IMPORT ' in line:
                    file = line.split('IMPORT ', 1)[-1]
                    file = file.replace('"', "")
                    file = file.replace("\n", "")
                    file = file.replace(".para", "")
                    file = file.replace(".", "/")
                    file += ".para"
                    for q in imported:
                      if file == q:
                        isImported = True
                    if not isImported:
                      if code2 != "":
                        code2 += "\n"
                      codelines2f = None
                      try:
                        codelines2f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines2f = open(file, "r")
                      codelines2 = codelines2f.read()
                      codelines2f.close()
                      code2 += codelines2
                
                      code = code.replace(line, "")
                      imported.append(file)
                    
                    isImported = False
                  elif 'IMPORTend ' in line:
                    file = line.split('IMPORTend ', 1)[-1]
                    file = file.replace('"', "")
                    file = file.replace("\n", "")
                    file = file.replace(".para", "")
                    file = file.replace(".", "/")
                    file += ".para"
                    for q in imported:
                      if file == q:
                        isImported = True
                    if not isImported:
                      if code3 != "":
                        code3 += "\n"
                      codelines3f = None
                      try:
                        codelines3f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines3f = open(file, "r")
                      codelines3 = codelines3f.readlines()
                      codelines3f.close()
                      for line3 in codelines3:
                        code3 += line3
                
                      code = code.replace(line, "")
                      imported.append(file)
                
                    isImported = False
                  # else:
                  #   # code += line[:-1]
                  #   code += line
                
                  codelines = code.splitlines()
                
                while any("IMPORT " in s for s in code2.splitlines()):
                  for line in code2.splitlines():
                    if line.replace("	", "").replace(" ", "").startswith("#"):
                      code2 = code2.replace(line, "")
                    elif 'IMPORT ' in line:
                      file = line.split('IMPORT ', 1)[-1]
                      file = file.replace('"', "")
                      file = file.replace("\n", "")
                      file = file.replace(".para", "")
                      file = file.replace(".", "/")
                      file += ".para"
                      if code2 != "":
                        code2 += "\n"
                      codelines2f = None
                      try:
                        codelines2f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines2f = open(file, "r")
                      codelines2 = codelines2f.readlines()
                      codelines2f.close()
                      for line2 in codelines2:
                        code2 += line2
                
                      code2 = code2.replace(line, "")
                    elif 'IMPORTend ' in line:
                      file = line.split('IMPORTend ', 1)[-1]
                      file = file.replace('"', "")
                      file = file.replace("\n", "")
                      file = file.replace(".para", "")
                      file = file.replace(".", "/")
                      file += ".para"
                      if code3 != "":
                        code3 += "\n"
                      codelines3f = None
                      try:
                        codelines3f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines3f = open(file, "r")
                      codelines3 = codelines3f.readlines()
                      codelines3f.close()
                      for line3 in codelines3:
                        code3 += line3
                
                      code2 = code2.replace(line, "")
                    # else:
                    #   # code += line[:-1]
                    #   code2 += line
                
                while any("IMPORT " in s for s in code3.splitlines()):
                  for line in code3.splitlines():
                    if line.replace("	", "").replace(" ", "").startswith("#"):
                      code3 = code3.replace(line, "")
                    elif 'IMPORT ' in line:
                      file = line.split('IMPORT ', 1)[-1]
                      file = file.replace('"', "")
                      file = file.replace("\n", "")
                      file = file.replace(".para", "")
                      file = file.replace(".", "/")
                      file += ".para"
                      if code2 != "":
                        code2 += "\n"
                      codelines2f = None
                      try:
                        codelines2f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines2f = open(file, "r")
                      codelines2 = codelines2f.readlines()
                      codelines2f.close()
                      for line2 in codelines2:
                        code2 += line2
                
                      code3 = code3.replace(line, "")
                    elif 'IMPORTend ' in line:
                      file = line.split('IMPORTend ', 1)[-1]
                      file = file.replace('"', "")
                      file = file.replace("\n", "")
                      file = file.replace(".para", "")
                      file = file.replace(".", "/")
                      file += ".para"
                      if code3 != "":
                        code3 += "\n"
                      codelines3f = None
                      try:
                        codelines3f = open(file, "r")
                      except:
                        file =+ "code"
                        codelines3f = open(file, "r")
                      codelines3 = codelines3f.readlines()
                      codelines3f.close()
                      for line3 in codelines3:
                        # code3 += line3[:-1]
                        code3 += line3
                
                        code3 = code3.replace(line, "")
                    # else:
                    #   # code += line[:-1]
                    #   code3 += line
                if code2 != "":
                  code2 += code
                  code = code2
                if code3 != "":
                  code += code3
                script = code
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))

        return RTResult().success(Number.null)

    execute_run.arg_names = ["fn"]


BuiltInFunction.modulo = BuiltInFunction("modulo")
BuiltInFunction.indexof = BuiltInFunction("indexof")
OptionalFunction.print = OptionalFunction("print")
OptionalFunction.paragameinit = OptionalFunction("paragameinit")

BuiltInFunction.stairs = BuiltInFunction("stairs")
BuiltInFunction.halfDiamondStar = BuiltInFunction("halfDiamondStar")
BuiltInFunction.removepunc = BuiltInFunction("removepunc")
BuiltInFunction.removeletters = BuiltInFunction("removeletters")
BuiltInFunction.removenumbers = BuiltInFunction("removenumbers")
BuiltInFunction.removespaces = BuiltInFunction("removespaces")
BuiltInFunction.removeallspaces = BuiltInFunction("removeallspaces")
BuiltInFunction.keeppunc = BuiltInFunction("keeppunc")
OptionalFunction.randomnumber = OptionalFunction("randomnumber")
BuiltInFunction.cryptogeneratekey = BuiltInFunction("cryptogeneratekey")
BuiltInFunction.cryptoencrypt = BuiltInFunction("cryptoencrypt")
BuiltInFunction.cryptodecrypt = BuiltInFunction("cryptodecrypt")
BuiltInFunction.cryptoencode = BuiltInFunction("cryptoencode")
BuiltInFunction.cryptodecode = BuiltInFunction("cryptodecode")
BuiltInFunction.printColor = BuiltInFunction("printColor")
BuiltInFunction.recognizer = BuiltInFunction("recognizer")
BuiltInFunction.microphone = BuiltInFunction("microphone")
BuiltInFunction.translator = BuiltInFunction("translator")
BuiltInFunction.translate = BuiltInFunction("translate")
BuiltInFunction.print_ret = BuiltInFunction("print_ret")
OptionalFunction.discordclient = OptionalFunction("discordclient")
OptionalFunction.discordtoken = OptionalFunction("discordtoken")
OptionalFunction.ondiscordbotready = OptionalFunction("ondiscordbotready")
OptionalFunction.ondiscordbotmessage = OptionalFunction("ondiscordbotmessage")
OptionalFunction.discordbotsendmessage = OptionalFunction("discordbotsendmessage")
OptionalFunction.rundiscordbot = OptionalFunction("rundiscordbot")
BuiltInFunction.debuglog = BuiltInFunction("debuglog")
BuiltInFunction.debugwarning = BuiltInFunction("debugwarning")
BuiltInFunction.debugerror = BuiltInFunction("debugerror")
BuiltInFunction.debugwarn = BuiltInFunction("debugwarn")
BuiltInFunction.debugerr = BuiltInFunction("debugerr")
BuiltInFunction.debugfatal = BuiltInFunction("debugfatal")
BuiltInFunction.app = BuiltInFunction("app")
BuiltInFunction.tk = BuiltInFunction("tk")
# BuiltInFunction.label       = BuiltInFunction("label")
# OptionalFunction.label       = OptionalFunction("label")
BuiltInFunction.coloredlabel = BuiltInFunction("coloredlabel")
# BuiltInFunction.poslabel       = BuiltInFunction("poslabel")
# BuiltInFunction.poscollabel       = BuiltInFunction("poscollabel")
BuiltInFunction.mainloop = BuiltInFunction("mainloop")
BuiltInFunction.mainloopapp = BuiltInFunction("mainloopapp")
BuiltInFunction.demoapp = BuiltInFunction("demoapp")
BuiltInFunction.turtle = BuiltInFunction("turtle")
BuiltInFunction.turtlescreen = BuiltInFunction("turtlescreen")
BuiltInFunction.turtleright = BuiltInFunction("turtleright")
BuiltInFunction.turtleleft = BuiltInFunction("turtleleft")
BuiltInFunction.turtleup = BuiltInFunction("turtleup")
BuiltInFunction.turtledown = BuiltInFunction("turtledown")
BuiltInFunction.turtlehide = BuiltInFunction("turtlehide")
BuiltInFunction.turtlependown = BuiltInFunction("turtlependown")
BuiltInFunction.turtlewidth = BuiltInFunction("turtlewidth")
BuiltInFunction.turtlecircle = BuiltInFunction("turtlecircle")
BuiltInFunction.turtlespeed = BuiltInFunction("turtlespeed")
BuiltInFunction.turtlepenup = BuiltInFunction("turtlepenup")
BuiltInFunction.turtlebackward = BuiltInFunction("turtlebackward")
BuiltInFunction.turtleforward = BuiltInFunction("turtleforward")
BuiltInFunction.turtletitle = BuiltInFunction("turtletitle")
BuiltInFunction.turtlecolor = BuiltInFunction("turtlecolor")
BuiltInFunction.turtlefillcolor = BuiltInFunction("turtlefillcolor")
BuiltInFunction.turtleposition = BuiltInFunction("turtleposition")
BuiltInFunction.turtlebgcolor = BuiltInFunction("turtlebgcolor")
BuiltInFunction.turtlepencolor = BuiltInFunction("turtlepencolor")
BuiltInFunction.turtleexitonclick = BuiltInFunction("turtleexitonclick")
BuiltInFunction.turtleheading = BuiltInFunction("turtleheading")
BuiltInFunction.turtlepen = BuiltInFunction("turtlepen")
BuiltInFunction.openfile = BuiltInFunction("openfile")
BuiltInFunction.closefile = BuiltInFunction("closefile")
BuiltInFunction.openfilemode = BuiltInFunction("openfilemode")
BuiltInFunction.readfile = BuiltInFunction("readfile")
BuiltInFunction.readpartfile = BuiltInFunction("readpartfile")
BuiltInFunction.readfileline = BuiltInFunction("readfileline")
BuiltInFunction.writefile = BuiltInFunction("writefile")
BuiltInFunction.appendfile = BuiltInFunction("appendfile")
BuiltInFunction.createfile = BuiltInFunction("createfile")
BuiltInFunction.deletefile = BuiltInFunction("deletefile")
BuiltInFunction.deletedirectory = BuiltInFunction("deletedirectory")
BuiltInFunction.fileexists = BuiltInFunction("fileexists")
# BuiltInFunction.join = BuiltInFunction("join")
BuiltInFunction.gettime = BuiltInFunction("gettime")
BuiltInFunction.getsecond = BuiltInFunction("getsecond")
BuiltInFunction.getminute = BuiltInFunction("getminute")
BuiltInFunction.gethour = BuiltInFunction("gethour")
BuiltInFunction.getdate = BuiltInFunction("getdate")
BuiltInFunction.getdatetime = BuiltInFunction("getdatetime")
BuiltInFunction.getday = BuiltInFunction("getday")
BuiltInFunction.getmonth = BuiltInFunction("getmonth")
BuiltInFunction.getyear = BuiltInFunction("getyear")
BuiltInFunction.replace = BuiltInFunction("replace")
BuiltInFunction.replacefirst = BuiltInFunction("replacefirst")
BuiltInFunction.loop = BuiltInFunction("loop")
OptionalFunction.input = OptionalFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.run = BuiltInFunction("run")
BuiltInFunction.convert = BuiltInFunction("convert")
# OptionalFunction.Import = OptionalFunction("Import")


#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MODULO:
            result, error = left % right
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(
            node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("NONE", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("MODULO", BuiltInFunction.modulo)
global_symbol_table.set("INDEXOF", BuiltInFunction.indexof)
global_symbol_table.set("PRINT", OptionalFunction.print)
global_symbol_table.set("PARAGAMEINIT", OptionalFunction.paragameinit)
global_symbol_table.set("APP", BuiltInFunction.app)
global_symbol_table.set("TK", BuiltInFunction.tk)
# global_symbol_table.set("LABEL", BuiltInFunction.label)
# global_symbol_table.set("LABEL", OptionalFunction.label)
global_symbol_table.set("COLOREDLABEL", BuiltInFunction.coloredlabel)
global_symbol_table.set("COLOUREDLABEL", BuiltInFunction.coloredlabel)
global_symbol_table.set("COLLABEL", BuiltInFunction.coloredlabel)
# global_symbol_table.set("POSLABEL", BuiltInFunction.poslabel)
# global_symbol_table.set("POSCOLLABEL", BuiltInFunction.poscollabel)
global_symbol_table.set("MAINLOOP", BuiltInFunction.mainloop)
global_symbol_table.set("MAINLOOPAPP", BuiltInFunction.mainloopapp)
global_symbol_table.set("DEMOAPP", BuiltInFunction.demoapp)
global_symbol_table.set("TURTLE", BuiltInFunction.turtle)
global_symbol_table.set("TURTLESCREEN", BuiltInFunction.turtlescreen)
global_symbol_table.set("TURTLERIGHT", BuiltInFunction.turtleright)

global_symbol_table.set("TURTLELEFT", BuiltInFunction.turtleleft)
global_symbol_table.set("TURTLEUP", BuiltInFunction.turtleup)
global_symbol_table.set("TURTLEDOWN", BuiltInFunction.turtledown)
global_symbol_table.set("TURTLEHIDE", BuiltInFunction.turtlehide)
global_symbol_table.set("TURTLEPENDOWN", BuiltInFunction.turtlependown)
global_symbol_table.set("TURTLEWIDTH", BuiltInFunction.turtlewidth)
global_symbol_table.set("TURTLECIRCLE", BuiltInFunction.turtlecircle)
global_symbol_table.set("TURTLESPEED", BuiltInFunction.turtlespeed)
global_symbol_table.set("TURTLEPENUP", BuiltInFunction.turtlepenup)
global_symbol_table.set("TURTLEBACKWARD", BuiltInFunction.turtlebackward)
global_symbol_table.set("TURTLEFORWARD", BuiltInFunction.turtleforward)
global_symbol_table.set("TURTLETITLE", BuiltInFunction.turtletitle)
global_symbol_table.set("TURTLECOLOR", BuiltInFunction.turtlecolor)
global_symbol_table.set("TURTLEFILLCOLOR", BuiltInFunction.turtlefillcolor)
global_symbol_table.set("TURTLEHEADING", BuiltInFunction.turtleheading)
global_symbol_table.set("TURTLEPOSITION", BuiltInFunction.turtleposition)
global_symbol_table.set("TURTLEBGCOLOR", BuiltInFunction.turtlebgcolor)
global_symbol_table.set("TURTLEPENCOLOR", BuiltInFunction.turtlepencolor)
global_symbol_table.set("TURTLEEXITONCLICK", BuiltInFunction.turtleexitonclick)
global_symbol_table.set("TURTLEPEN", BuiltInFunction.turtlepen)
global_symbol_table.set("PRINTCOLOR", BuiltInFunction.printColor)
global_symbol_table.set("RECOGNIZER", BuiltInFunction.recognizer)
global_symbol_table.set("MICROPHONE", BuiltInFunction.microphone)
global_symbol_table.set("TRANSLATOR", BuiltInFunction.translator)
global_symbol_table.set("TRANSLATE", BuiltInFunction.translate)

global_symbol_table.set("STAIRS", BuiltInFunction.stairs)
global_symbol_table.set("HALFDIAMONDSTAR", BuiltInFunction.halfDiamondStar)
global_symbol_table.set("REMOVEPUNC", BuiltInFunction.removepunc)
global_symbol_table.set("REMOVEPUNCTUATION", BuiltInFunction.removepunc)
global_symbol_table.set("REMOVELETTERS", BuiltInFunction.removeletters)
global_symbol_table.set("REMOVELETTER", BuiltInFunction.removeletters)
global_symbol_table.set("REMOVENUMBERS", BuiltInFunction.removenumbers)
global_symbol_table.set("REMOVENUMBER", BuiltInFunction.removenumbers)
global_symbol_table.set("REMOVESPACES", BuiltInFunction.removespaces)
global_symbol_table.set("REMOVESPACE", BuiltInFunction.removespaces)
global_symbol_table.set("REMOVEALLSPACES", BuiltInFunction.removeallspaces)
global_symbol_table.set("REMOVEALLSPACE", BuiltInFunction.removeallspaces)
global_symbol_table.set("KEEPPUNC", BuiltInFunction.keeppunc)
global_symbol_table.set("KEEPPUNCTUATION", BuiltInFunction.keeppunc)
global_symbol_table.set("RANDOMNUMBER", OptionalFunction.randomnumber)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("DISCORDCLIENT", OptionalFunction.discordclient)
global_symbol_table.set("DISCORDTOKEN", OptionalFunction.discordtoken)
global_symbol_table.set("ONDISCORDBOTREADY", OptionalFunction.ondiscordbotready)
global_symbol_table.set("ONDISCORDBOTMESSAGE", OptionalFunction.ondiscordbotmessage)
global_symbol_table.set("DISCORDBOTSENDMESSAGE", OptionalFunction.discordbotsendmessage)
global_symbol_table.set("RUNDISCORDBOT", OptionalFunction.rundiscordbot)
global_symbol_table.set("CRYPTOGENERATEKEY", BuiltInFunction.cryptogeneratekey)
global_symbol_table.set("CRYPTOENCRYPT", BuiltInFunction.cryptoencrypt)
global_symbol_table.set("CRYPTODECRYPT", BuiltInFunction.cryptodecrypt)
global_symbol_table.set("CRYPTOENCODE", BuiltInFunction.cryptoencode)
global_symbol_table.set("CRYPTODECODE", BuiltInFunction.cryptodecode)
global_symbol_table.set("ECHO", OptionalFunction.print)
global_symbol_table.set("ECHOCOLOR", BuiltInFunction.printColor)
global_symbol_table.set("DEBUGLOG", BuiltInFunction.debuglog)
global_symbol_table.set("DEBUGWARNING", BuiltInFunction.debugwarning)
global_symbol_table.set("DEBUGERROR", BuiltInFunction.debugerror)
global_symbol_table.set("DEBUGWARN", BuiltInFunction.debugwarn)
global_symbol_table.set("DEBUGERR", BuiltInFunction.debugerr)
global_symbol_table.set("DEBUGFATAL", BuiltInFunction.debugfatal)
global_symbol_table.set("OPENFILE", BuiltInFunction.openfile)
global_symbol_table.set("CLOSEFILE", BuiltInFunction.closefile)
global_symbol_table.set("OPENFILEMODE", BuiltInFunction.openfilemode)
global_symbol_table.set("READFILE", BuiltInFunction.readfile)
global_symbol_table.set("READPARTFILE", BuiltInFunction.readpartfile)
global_symbol_table.set("READFILELINE", BuiltInFunction.readfileline)
global_symbol_table.set("WRITEFILE", BuiltInFunction.writefile)
global_symbol_table.set("APPENDFILE", BuiltInFunction.appendfile)
global_symbol_table.set("CREATEFILE", BuiltInFunction.createfile)
global_symbol_table.set("DELETEFILE", BuiltInFunction.deletefile)
global_symbol_table.set("DELETEDIRECTORY", BuiltInFunction.deletedirectory)
global_symbol_table.set("FILEEXISTS", BuiltInFunction.fileexists)
# global_symbol_table.set("JOIN", BuiltInFunction.join)
global_symbol_table.set("GETTIME", BuiltInFunction.gettime)
global_symbol_table.set("GETSECOND", BuiltInFunction.getsecond)
global_symbol_table.set("GETMINUTE", BuiltInFunction.getminute)
global_symbol_table.set("GETHOUR", BuiltInFunction.gethour)
global_symbol_table.set("GETDATE", BuiltInFunction.getdate)
global_symbol_table.set("GETDATETIME", BuiltInFunction.getdatetime)
global_symbol_table.set("GETDAY", BuiltInFunction.getday)
global_symbol_table.set("GETMONTH", BuiltInFunction.getmonth)
global_symbol_table.set("GETYEAR", BuiltInFunction.getyear)
global_symbol_table.set("REPLACE", BuiltInFunction.replace)
global_symbol_table.set("REPLACEFIRST", BuiltInFunction.replacefirst)
global_symbol_table.set("LOOP", BuiltInFunction.loop)
global_symbol_table.set("INPUT", OptionalFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("INPUTINT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("CLS", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_NUMBER", BuiltInFunction.is_number)
global_symbol_table.set("ISNUM", BuiltInFunction.is_number)
global_symbol_table.set("ISNUMBER", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_STRING", BuiltInFunction.is_string)
global_symbol_table.set("ISSTR", BuiltInFunction.is_string)
global_symbol_table.set("ISSTRING", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("ISLIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUNC", BuiltInFunction.is_function)
global_symbol_table.set("IS_FUNCTION", BuiltInFunction.is_function)
global_symbol_table.set("ISFUNC", BuiltInFunction.is_function)
global_symbol_table.set("ISFUNCTION", BuiltInFunction.is_function)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)
global_symbol_table.set("LEN", BuiltInFunction.len)
global_symbol_table.set("RUN", BuiltInFunction.run)


# global_symbol_table.set("CONVERT", BuiltInFunction.convert)
# global_symbol_table.set("IMPORT", OptionalFunction.Import)

def run(fn, text):
    # global importing

    # if "IMPORT" in text:
        # importing = False
    # else:
        # importing = True
    # if not importing:
    # sys.stdout = open(os.devnull, 'w')
    
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    
    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    # run(fn, text)
    return result.value, result.error
    # else:
    #     #sys.stdout = originalStdout

    #     # Generate tokens
    #     lexer = Lexer(fn, text)
    #     tokens, error = lexer.make_tokens()
    #     if error: return None, error

    #     # Generate AST
    #     parser = Parser(tokens)
    #     ast = parser.parse()
    #     if ast.error: return None, ast.error
    
    #     # Run program
    #     interpreter = Interpreter()
    #     context = Context('<program>')
    #     context.symbol_table = global_symbol_table
    #     result = interpreter.visit(ast.node, context)

    #     #importing = False

    #     return result.value, result.error

