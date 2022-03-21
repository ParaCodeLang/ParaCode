#pragma once

#include <boost/any.hpp>

class Keywords {
public:
    static std::map<std::string, boost::any> s_Values;

    static boost::any Let;
    static boost::any If;
    static boost::any Else;
    static boost::any Elif;
    static boost::any Func;
    static boost::any Import;
    static boost::any Return;
    static boost::any While;
    static boost::any For;
    static boost::any In;
    static boost::any Macro;
    static boost::any Mixin;
    static boost::any Try;
    static boost::any Catch;
    static boost::any Finally;
};

class TokenType {
public:
    static std::map<std::string, boost::any> s_Values;

    static boost::any NoneToken;

    static boost::any LParen;
    static boost::any RParen;
    static boost::any LBrace;
    static boost::any RBrace;
    static boost::any LBracket;
    static boost::any RBracket;
    static boost::any Plus;
    static boost::any Minus;
    static boost::any Multiply;
    static boost::any Exponentiation;
    static boost::any Divide;
    static boost::any Equals;
    static boost::any Semicolon;
    static boost::any Colon;
    static boost::any Dot;
    static boost::any Comma;
    static boost::any Not;
    static boost::any Question;
    static boost::any Modulus;
    static boost::any LessThan;
    static boost::any LessThanEqual;
    static boost::any GreaterThan;
    static boost::any GreaterThanEqual;

    static boost::any And;
    static boost::any Or;
    
    static boost::any BitwiseOr;
    static boost::any BitwiseAnd;
    static boost::any BitwiseXor;
    static boost::any BitwiseNot;
    static boost::any BitwiseLShift;
    static boost::any BitwiseRShift;
    
    static boost::any Compare;
    static boost::any NotCompare;
    static boost::any Spaceship;

    static boost::any Arrow;
    
    static boost::any PlusEquals;
    static boost::any MinusEquals;
    static boost::any MultiplyEquals;
    static boost::any DivideEquals;
    static boost::any ModulusEquals;
    static boost::any BitwiseOrEquals;
    static boost::any BitwiseAndEquals;
    static boost::any BitwiseXorEquals;
    static boost::any BitwiseLShiftEquals;
    static boost::any BitwiseRShiftEquals;
    
    static boost::any Identifier;
    static boost::any Number;
    static boost::any String;
    static boost::any Keyword;

    boost::any getType(std::string value) {
        if (value == "") {
            return nullptr;
        }

        if (TokenType::s_Values.count(value)) {
            return TokenType::s_Values[value];
        }
        
        if (isdigit(value[0]) || value[0] == '.') {
            // what?
            if (value.length() > 1) {
                if (value[1] == 'x' or value[1] == 'X') {
                    return TokenType::Number;
                }
            }
                    
            if (value.find('.') != std::string::npos) {
                return TokenType::Number;
            }
            return TokenType::Number;
        }
        else if ((value[0] == '"' && value.back() == '"') || (value[0] == '\'' && value.back() == '\'')) {
            return TokenType::String;
        }

        // check if string is keyword
        if (Keywords::s_Values.count(value)) {
            return TokenType::Keyword;
        }

        // nothing else, must be identifier
        return TokenType::Identifier;
    }

    bool hasValue(std::string value) {
        return TokenType::s_Values.count(value);
    }
};

// class LexerToken():
//     def __init__(self, value, token_type=None):
//         if token_type is None:
//             self.type = TokenType.get_type(TokenType, value)
//         else:
//             self.type = token_type
//         self.value = value
//         self.location = (0, 0)
//     def __str__(self):
//         return "LexerToken[Type:{0}, Value:'{1}']".format(self.type, self.value)
//     def __repr__(self):
//         return self.__str__()
