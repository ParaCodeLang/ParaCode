#pragma once

#include "util.h"
#include "parse/source_location.h"

#include <boost/any.hpp>

class Keywords {
public:
    static std::map<std::string, Keywords> s_Values;

    static Keywords Let;
    static Keywords If;
    static Keywords Else;
    static Keywords Elif;
    static Keywords Func;
    static Keywords Import;
    static Keywords Return;
    static Keywords While;
    static Keywords For;
    static Keywords In;
    static Keywords Macro;
    static Keywords Mixin;
    static Keywords Try;
    static Keywords Catch;
    static Keywords Finally;

    std::string name;
    boost::any value;

    inline bool operator==(const Keywords& rhs) { return this->name == rhs.name; }
    inline bool operator!=(const Keywords& rhs) { return !(*this == rhs); }

    Keywords() = default;
    Keywords(std::string name, boost::any value) {
        this->name = name;
        this->value = value;
    }
    Keywords(std::string name) {
        this->name = name;
        this->value = Keywords::s_Values[name];
    }
};

class TokenType {
public:
    static std::map<std::string, TokenType> s_Values;

    static TokenType NoneToken;

    static TokenType LParen;
    static TokenType RParen;
    static TokenType LBrace;
    static TokenType RBrace;
    static TokenType LBracket;
    static TokenType RBracket;
    static TokenType Plus;
    static TokenType Minus;
    static TokenType Multiply;
    static TokenType Exponentiation;
    static TokenType Divide;
    static TokenType Equals;
    static TokenType Semicolon;
    static TokenType Colon;
    static TokenType Dot;
    static TokenType Comma;
    static TokenType Not;
    static TokenType Question;
    static TokenType Modulus;
    static TokenType LessThan;
    static TokenType LessThanEqual;
    static TokenType GreaterThan;
    static TokenType GreaterThanEqual;

    static TokenType And;
    static TokenType Or;
    
    static TokenType BitwiseOr;
    static TokenType BitwiseAnd;
    static TokenType BitwiseXor;
    static TokenType BitwiseNot;
    static TokenType BitwiseLShift;
    static TokenType BitwiseRShift;
    
    static TokenType Compare;
    static TokenType NotCompare;
    static TokenType Spaceship;

    static TokenType Arrow;
    
    static TokenType PlusEquals;
    static TokenType MinusEquals;
    static TokenType MultiplyEquals;
    static TokenType DivideEquals;
    static TokenType ModulusEquals;
    static TokenType BitwiseOrEquals;
    static TokenType BitwiseAndEquals;
    static TokenType BitwiseXorEquals;
    static TokenType BitwiseLShiftEquals;
    static TokenType BitwiseRShiftEquals;
    
    static TokenType Identifier;
    static TokenType Number;
    static TokenType String;
    static TokenType Keyword;

    std::string name;
    boost::any value;

    TokenType() = default;
    TokenType(std::string name, boost::any value) {
        this->name = name;
        this->value = value;
    }

    inline bool operator==(const TokenType& rhs) { return this->name == rhs.name; }
    inline bool operator!=(const TokenType& rhs) { return !(*this == rhs); }

    static TokenType* getType(std::string value);
    static bool hasValue(std::string value);

    std::string toString() const {
        std::string result = "TokenType::" + name;
        return result;
    }
};

class LexerToken {
public:
    static LexerToken* NONE;

    TokenType* type;

    std::string value;
    std::tuple<int, int> location;

    LexerToken(std::string value, TokenType* tokenType = nullptr) {
        if (tokenType == nullptr) {
            this->type = TokenType::getType(value);
        }
        else {
            this->type = tokenType;
        }
        this->value = value;
        this->location = std::make_tuple(0, 0);
    }
};

class Lexer {
public:
    std::vector<LexerToken*> tokens;
    std::string data;
    std::string tokenData;
    int index;
    SourceLocation sourceLocation;

    Lexer(std::string data, SourceLocation sourceLocation) {
        this->tokens = {};
        this->data = data;
        this->tokenData = "";
        this->index = 0;
        this->sourceLocation = sourceLocation;
        
        // Error handling
        this->sourceLocation.row = 1;
        this->sourceLocation.col = 1;
    }

    // Return character and progress through buffer
    const char readChar(int amt = 1) {
        if (this->index+amt > this->data.length()) {
            return '\0';
        }
        char rval = this->data[this->index];
        this->index += amt;
        this->sourceLocation.col += 1;
        if (rval == '\n') {
            this->sourceLocation.col = 1;
            this->sourceLocation.row += 1;
        }
        return rval;
    }

    // Return character and keep index
    const char peekChar(int offset = 1) {
        int idx = this->index + offset;
        if (idx >= this->data.length() || idx < 0) {
            return '\0';
        }
        return this->data[idx];
    }

    void pushToken() {
        LexerToken* token = new LexerToken(this->tokenData);
        if (this->tokenData == "") {
            throw std::runtime_error("tokendata blank");
        }
        token->location = this->sourceLocation.colRow();
        this->tokens.push_back(token);
        this->tokenData = "";
    }

    bool skipWhitespace() {
        if (Util::isSpaces(std::string(1, this->peekChar(0)))) {
            while (Util::isSpaces(std::string(1, this->peekChar(0)))) {
                this->readChar();
            }
            return true;
        }
        return false;
    }

    std::vector<LexerToken*> lex() {
        std::string splitables = "(){}[];:+-*/=.,!?|&~<>^%";
        std::vector<std::string> multicharSplitables = {
            "**", "<=>", "<<=", ">>=",
            "|=", "&=", "^=",
            "==", "!=", "<=", ">=",
            "+=", "-=", "*=", "/=",
            "%=", "==", "!=", "->",
            "&&", "||", "<<", ">>"
        };

        std::map<char, char> escapeChars = {
            { 'n', '\n' },
            { 'b', '\b' },
            { 't', '\t' },
            { 'v', '\v' },
            { 'a', '\a' },
            { 'r', '\r' },
            { 'f', '\f' },
            // { 's', '\s' },
            // { "033", '\033' },
            { '\\', '\\' },
            { '\'', '\'' },
            { '"', '"' },
        };
        this->skipWhitespace();
        
        char stringType = '\0';

        while (this->peekChar(0) != '\0') {
            if (stringType && this->peekChar(0) == '\\') {
                // Skip '/'
                this->readChar();
                char escapeChar = this->readChar();
                if (escapeChars.count(escapeChar)) {
                    this->tokenData += escapeChars[escapeChar];
                }
                else {
                    std::cout << Util::format("Error: Unknown escape character '%s'", escapeChar) << std::endl;
                }
                continue;
            }

            // Comments
            if (stringType == '\0' && (this->peekChar(0) == '#' || (this->peekChar(0) == '/' && this->peekChar(1) == '/') or (this->peekChar(0) == '/' and this->peekChar(1) == '*'))) {
                this->readChar();
                if (this->peekChar(-1) == '#' && this->peekChar(0) == '*') {
                    // Multiline comment

                    // Skip '*' character
                    this->readChar();

                    // Read until '*#'
                    while (this->readChar() != '*' && this->peekChar(1) != '#') {
                        // EOF
                        if (this->peekChar(0) == '\0') {
                            break;
                        }
                    }

                    // Skip '*#' characters
                    this->readChar(2);

                    // End by pushing the token and skipping any whitespace afterwards
                    if (this->tokenData != "") {
                        this->pushToken();
                    }
                    this->skipWhitespace();
                }
                else if (this->peekChar(-1) == '/' && this->peekChar(0) == '*') {
                    // Multiline comment

                    // Skip '*' character
                    this->readChar();

                    // Read until '*/'
                    while (this->readChar() != '*' && this->peekChar(1) != '/') {
                        // EOF
                        if (this->peekChar(0) == '\0') {
                            break;
                        }
                    }

                    // Skip '*/' characters
                    this->readChar(2);

                    // End by pushing the token and skipping any whitespace afterwards
                    if (this->tokenData != "") {
                        this->pushToken();
                    }
                    this->skipWhitespace();
                }
                else {
                    while (this->readChar() != '\n') {
                        // EOF
                        if (this->peekChar(0) == '\0') {
                            break;
                        }
                        // Skip any whitespace after comment
                        this->skipWhitespace();
                    }
                }
                continue;
            }

            // Encountered whitespace and not in string, push token
            else if (stringType == '\0' && this->skipWhitespace()) {
                this->pushToken();
                continue;
            }

            else if (splitables.find(this->peekChar(0)) != std::string::npos && stringType == '\0') {
                if (!Util::isSpaces(std::string(1, this->peekChar(-1))) && splitables.find(this->peekChar(-1)) == std::string::npos && this->tokenData.length() > 0) {
                    this->pushToken();
                }

                bool multichar = false;
                for (std::string tok : multicharSplitables) {
                    int idx = this->data.find(this->data.substr(this->index, this->index+tok.length()));
                    if (idx != std::string::npos) {
                        for (int i = 0; i < tok.length(); ++i) {
                            this->tokenData += this->readChar();
                        }

                        multichar = true;
                    }
                }

                // if (Util::isDigits(this->peekChar(-1)) && this->peekChar(0) == ".") {
                //     this->tokenData += this->readChar();
                //     continue;
                // }

                if (!multichar) {
                    this->tokenData = this->readChar();
                }

                this->pushToken();
                this->skipWhitespace();
                continue;
            }

            else if (Util::isDigits(std::string(1, this->peekChar(0))) && stringType == '\0') {
                bool isFloat = false;

                while (Util::isDigits(std::string(1, this->peekChar(0)))) {
                    this->tokenData += this->readChar();

                    if (!isFloat && this->peekChar(0) == '.') {
                        // if next char is identifier, its not float,
                        // rather it could be something like
                        // `1.to_str()`
                        if (!Util::isDigits(std::string(1, this->peekChar(1)))) {
                            break;
                        }

                        this->tokenData += this->readChar();
                        isFloat = false;
                    }
                }

                this->pushToken();
                this->skipWhitespace();
                continue;
            }

            // Check if string character
            if (this->peekChar(0) == '"') {
                // If currently in double quotes string, end and set stringType to null
                if (stringType == '"') {
                    stringType = '\0';
                }
                // If no string is open, open a new one
                else if (stringType == '\0') {
                    stringType = '"';
                }
                // If currently in single quotes string, ignore
            }
            else if (this->peekChar(0) == '\'') {
                if (stringType == '\'') {
                    stringType = '\0';
                }
                else if (stringType == '\0') {
                    stringType = '\'';
                }
            }

            this->tokenData += this->readChar();
        }
        // Still some data left in tokenData, push to end
        if (this->tokenData != "") {
            this->pushToken();
        }

        return this->tokens;
    }
};
