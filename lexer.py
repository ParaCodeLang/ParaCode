from enum import Enum, auto
from parse.source_location import SourceLocation

class Keywords(Enum):
    Let = 'let'
    If = 'if'
    Else = 'else'
    Elif = 'elif'
    Func = 'func'
    Import = 'import'
    Return = 'return'
    While = 'while'
    For = 'for'
    In = 'in'
    Macro = 'macro'
    Mixin = 'mixin'

class TokenType(Enum):
    NoneToken = auto()

    LParen = '('
    RParen = ')'
    LBrace = '{'
    RBrace = '}'
    LBracket = '['
    RBracket = ']'
    Plus = '+'
    Minus = '-'
    Multiply = '*'
    Divide = '/'
    Equals = '='
    Semicolon = ';'
    Colon = ':'
    Dot = '.'
    Comma = ','
    Not = '!'
    Modulus = '%'
    LessThan = '<'
    LessThanEqual = '<='
    GreaterThan = '>'
    GreaterThanEqual = '>='

    And = '&&'
    Or = '||'
    
    BitwiseOr = '|'
    BitwiseAnd = '&'
    BitwiseXor = '^'
    BitwiseNot = '~'
    
    Compare = '=='
    NotCompare = '!='
    Spaceship = '<=>'

    Arrow = '->'
    
    PlusEquals = '+='
    MinusEquals = '-='
    MultiplyEquals = '*='
    DivideEquals = '/='
    
    BitwiseLShift = auto()
    BitwiseRShift = auto()
    
    Identifier = auto()
    Number = auto()
    String = auto()
    Keyword = auto()

    def get_type(self, value):
        if value == '':
            return None
            
        if (value in self._value2member_map_):
            return TokenType(value)

        if value[0].isdigit() or value[0] == '.':
            # what?
            if len(value) > 1:
                if value[1] == 'x' or value[1] == 'X':
                    return TokenType.Number
                    
            if '.' in value:
                return TokenType.Number
            return TokenType.Number
        
        elif (value[0] == '"' and value[-1] == '"') or (value[0] == '\'' and value[-1] == '\''):
            return TokenType.String
        
        # check if string is keyword
        if value in Keywords._value2member_map_:
            return TokenType.Keyword
        
        # nothing else, must be identifier
        return TokenType.Identifier
        
    def has_value(self, value):
        # check if value exists in enum... wtf
        return value in self._value2member_map_

class LexerToken():
    def __init__(self, value, token_type=None):
        if token_type is None:
            self.type = TokenType.get_type(TokenType, value)
        else:
            self.type = token_type
        self.value = value
        self.location = (0, 0)
    def __str__(self):
        return "LexerToken[Type:{0}, Value:'{1}']".format(self.type, self.value)
    def __repr__(self):
        return self.__str__()

LexerToken.NONE = LexerToken('', TokenType.NoneToken)

class Lexer():
    def __init__(self, data, source_location):
        self.tokens = []
        self.data = data
        self.token_data = ""
        self.index = 0
        self.source_location = source_location
        
        # Error handling
        self.source_location.row = 1
        self.source_location.col = 1
    
    # return character and progress through buffer
    def read_char(self, amt=1):
        if self.index+amt > len(self.data):
            return ''
        rval = self.data[self.index]
        self.index += amt
        self.source_location.col += 1
        if rval == '\n':
            self.source_location.col = 1
            self.source_location.row += 1
        return rval
    
    # return character and keep index
    def peek_char(self, offset=1):
        idx = self.index+offset
        if idx >= len(self.data) or idx < 0:
            return ''
        return self.data[idx]
    
    def push_token(self):
        token = LexerToken(self.token_data)
        if self.token_data == '':
            raise Exception('tokendata blank')
        token.location = self.source_location.col_row
        self.tokens.append(token)
        self.token_data = ""
    
    def skip_whitespace(self):
        if self.peek_char(0).isspace():
            while self.peek_char(0).isspace():
                self.read_char()
            return True
        return False
    
    def lex(self):
        splitables = "(){}[];:+-*/=.,!|&~<>^%"
        multichar_splitables = [
            '<=>',
            '==', '!=', '<=', '>=',
            '+=', '-=', '*=', '/=',
            '==', '!=', '->',
            '&&', '||'
        ]
    
        escape_chars = {
            'n': '\n',
            'b': '\b',
            't': '\t',
            'v': '\v',
            'a': '\a',
            'r': '\r',
            '\\': '\\'
        }
        
        self.skip_whitespace()
        
        string_type = None
        
        while self.peek_char(0) != '':    
            if string_type and self.peek_char(0) == '\\':
                # skip '/'
                self.read_char()
                escape_char = self.read_char()
                if escape_char in escape_chars:
                    self.token_data += escape_chars[escape_char]
                else:
                    print("Error: Unknown escape character '{}'".format(escape_char))
                continue

            
            # multiline comments
            if self.peek_char(0) == '#' or (self.peek_char(0) == '/' and self.peek_char(1) == '/') or (self.peek_char(0) == '/' and self.peek_char(1) == '*'):
                self.read_char()
                if self.peek_char(-1) == '#' and self.peek_char(0) == '*':
                    # multiline comment
                    
                    # skip '*' character
                    self.read_char()
                    # read until '*#'
                    while (self.read_char() != '*' and self.peek_char(1) != '#'):
                        pass
                        
                    # skip '*#' characters
                    self.read_char(1)
                elif self.peek_char(-1) == '/' and self.peek_char(0) == '*':
                    # multiline comment
                    
                    # skip '*' character
                    self.read_char()
                    # read until '*/'
                    while (self.read_char() != '*' and self.peek_char(1) != '/'):
                        pass
                        
                    # skip '*/' characters
                    self.read_char(1)
                else:
                    while self.read_char() != '\n':
                        # EOF
                        if self.peek_char(0) == '':
                            break
                        
                # skip any whitespace after comment
                self.skip_whitespace()
                continue
                
            # encountered whitespace and not in string, push token
            elif string_type == None and self.skip_whitespace():
                self.push_token()
                continue
                  
            elif self.peek_char(0) in splitables and string_type == None:                    
                if not self.peek_char(-1).isspace() and self.peek_char(-1) not in splitables and len(self.token_data) > 0:
                    self.push_token()

                multichar = False

                for tok in multichar_splitables:
                    idx = self.data.find(tok, self.index, self.index+len(tok))
                    if idx != -1:
                        for i in range(len(tok)):
                            self.token_data += self.read_char()

                        multichar = True
                
                # if self.peek_char(-1).isdigit() and self.peek_char(0) == '.':
                #     self.token_data += self.read_char()
                #     continue
                    
                if not multichar:
                    self.token_data = self.read_char()

                self.push_token()
                self.skip_whitespace()
                continue
            elif self.peek_char(0).isdigit() and string_type == None:
                is_float = False

                while self.peek_char(0).isdigit():
                    self.token_data += self.read_char()

                    if not is_float and self.peek_char(0) == '.':
                        # if next char is identifier, its not float,
                        # rather it could be something like
                        # `1.to_str()`
                        if not self.peek_char(1).isdigit():
                            break

                        self.token_data += self.read_char()
                        is_float = True

                self.push_token()
                self.skip_whitespace()
                continue           
  
            # check if string character
            if (self.peek_char(0) == '"'):
                # if currently in double quotes string, end and set string_type to none
                if string_type == '"':
                    string_type = None
                # if no string is open, open a new one
                elif string_type == None:
                    string_type = '"'
                # if currently in single quotes string, ignore
                    
            elif (self.peek_char(0) == '\''):
                if string_type == '\'':
                    string_type = None
                elif string_type == None:
                    string_type = '\''

            
            self.token_data += self.read_char()
        # still some data left in token_data, push to end
        if self.token_data != '':
            self.push_token()

        return self.tokens
