#include "lexer.h"

Keywords Keywords::Let = Keywords("Let", "let");
Keywords Keywords::If = Keywords("If", "if");
Keywords Keywords::Else = Keywords("Else", "else");
Keywords Keywords::Elif = Keywords("Elif", "elif");
Keywords Keywords::Func = Keywords("Func", "func");
Keywords Keywords::Import = Keywords("Import", "import");
Keywords Keywords::Return = Keywords("Return", "return");
Keywords Keywords::While = Keywords("While", "while");
Keywords Keywords::For = Keywords("For", "for");
Keywords Keywords::In = Keywords("In", "in");
Keywords Keywords::Macro = Keywords("Macro", "macro");
Keywords Keywords::Mixin = Keywords("Mixin", "mixin");
Keywords Keywords::Try = Keywords("Try", "try");
Keywords Keywords::Catch = Keywords("Catch", "catch");
Keywords Keywords::Finally = Keywords("Finally", "finally");

std::map<std::string, Keywords> Keywords::s_Values = {
    { Keywords::Let.name, Keywords::Let },
    { Keywords::If.name, Keywords::If },
    { Keywords::Else.name, Keywords::Else },
    { Keywords::Elif.name, Keywords::Elif },
    { Keywords::Func.name, Keywords::Func },
    { Keywords::Import.name, Keywords::Import },
    { Keywords::Return.name, Keywords::Return },
    { Keywords::While.name, Keywords::While },
    { Keywords::For.name, Keywords::For },
    { Keywords::In.name, Keywords::In },
    { Keywords::Macro.name, Keywords::Macro },
    { Keywords::Mixin.name, Keywords::Mixin },
    { Keywords::Try.name, Keywords::Try },
    { Keywords::Catch.name, Keywords::Catch },
    { Keywords::Finally.name, Keywords::Finally }
};


TokenType TokenType::NoneToken = TokenType("NoneToken", 1);

TokenType TokenType::LParen = TokenType("LParen", "(");
TokenType TokenType::RParen = TokenType("RParen", ")");
TokenType TokenType::LBrace = TokenType("LBrace", "{");
TokenType TokenType::RBrace = TokenType("RBrace", "}");
TokenType TokenType::LBracket = TokenType("LBracket", "[");
TokenType TokenType::RBracket = TokenType("RBracket", "]");
TokenType TokenType::Plus = TokenType("Plus", "+");
TokenType TokenType::Minus = TokenType("Minus", "-");
TokenType TokenType::Multiply = TokenType("Multiply", "*");
TokenType TokenType::Exponentiation = TokenType("Exponentiation", "**");
TokenType TokenType::Divide = TokenType("Divide", "/");
TokenType TokenType::Equals = TokenType("Equals", "=");
TokenType TokenType::Semicolon = TokenType("Semicolon", ";");
TokenType TokenType::Colon = TokenType("Colon", ":");
TokenType TokenType::Dot = TokenType("Dot", ".");
TokenType TokenType::Comma = TokenType("Comma", ",");
TokenType TokenType::Not = TokenType("Not", "!");
TokenType TokenType::Question = TokenType("Question", "?");
TokenType TokenType::Modulus = TokenType("Modulus", "%");
TokenType TokenType::LessThan = TokenType("LessThan", "<");
TokenType TokenType::LessThanEqual = TokenType("LessThanEqual", "<=");
TokenType TokenType::GreaterThan = TokenType("GreaterThan", ">");
TokenType TokenType::GreaterThanEqual = TokenType("GreaterThanEqual", ">=");

TokenType TokenType::And = TokenType("And", "&&");
TokenType TokenType::Or = TokenType("Or", "||");

TokenType TokenType::BitwiseOr = TokenType("BitwiseOr", "|");
TokenType TokenType::BitwiseAnd = TokenType("BitwiseAnd", "&");
TokenType TokenType::BitwiseXor = TokenType("BitwiseXor", "^");
TokenType TokenType::BitwiseNot = TokenType("BitwiseNot", "~");
TokenType TokenType::BitwiseLShift = TokenType("BitwiseLShift", "<<");
TokenType TokenType::BitwiseRShift = TokenType("BitwiseRShift", ">>");

TokenType TokenType::Compare = TokenType("Compare", "==");
TokenType TokenType::NotCompare = TokenType("NotCompare", "!=");
TokenType TokenType::Spaceship = TokenType("Spaceship", "<=>");

TokenType TokenType::Arrow = TokenType("Arrow", "->");

TokenType TokenType::PlusEquals = TokenType("PlusEquals", "+=");
TokenType TokenType::MinusEquals = TokenType("MinusEquals", "-=");
TokenType TokenType::MultiplyEquals = TokenType("MultiplyEquals", "*=");
TokenType TokenType::DivideEquals = TokenType("DivideEquals", "/=");
TokenType TokenType::ModulusEquals = TokenType("ModulusEquals", "%=");
TokenType TokenType::BitwiseOrEquals = TokenType("BitwiseOrEquals", "|=");
TokenType TokenType::BitwiseAndEquals = TokenType("BitwiseAndEquals", "&=");
TokenType TokenType::BitwiseXorEquals = TokenType("BitwiseXorEquals", "^=");
TokenType TokenType::BitwiseLShiftEquals = TokenType("BitwiseLShiftEquals", "<<=");
TokenType TokenType::BitwiseRShiftEquals = TokenType("BitwiseRShiftEquals", ">>=");

TokenType TokenType::Identifier = TokenType("Identifier", 2);
TokenType TokenType::Number = TokenType("Number", 3);
TokenType TokenType::String = TokenType("String", 4);
TokenType TokenType::Keyword = TokenType("Keyword", 5);

std::map<std::string, TokenType> TokenType::s_Values = {
    { TokenType::NoneToken.name, TokenType::NoneToken },

    { TokenType::LParen.name, TokenType::LParen },
    { TokenType::RParen.name, TokenType::RParen },
    { TokenType::LBrace.name, TokenType::LBrace },
    { TokenType::RBrace.name, TokenType::RBrace },
    { TokenType::LBracket.name, TokenType::LBracket },
    { TokenType::RBracket.name, TokenType::RBracket },
    { TokenType::Plus.name, TokenType::Plus },
    { TokenType::Minus.name, TokenType::Minus },
    { TokenType::Multiply.name, TokenType::Multiply },
    { TokenType::Exponentiation.name, TokenType::Exponentiation },
    { TokenType::Divide.name, TokenType::Divide },
    { TokenType::Equals.name, TokenType::Equals },
    { TokenType::Semicolon.name, TokenType::Semicolon },
    { TokenType::Colon.name, TokenType::Colon },
    { TokenType::Dot.name, TokenType::Dot },
    { TokenType::Comma.name, TokenType::Comma },
    { TokenType::Not.name, TokenType::Not },
    { TokenType::Question.name, TokenType::Question },
    { TokenType::Modulus.name, TokenType::Modulus },
    { TokenType::LessThan.name, TokenType::LessThan },
    { TokenType::LessThanEqual.name, TokenType::LessThanEqual },
    { TokenType::GreaterThan.name, TokenType::GreaterThan },
    { TokenType::GreaterThanEqual.name, TokenType::GreaterThanEqual },

    { TokenType::And.name, TokenType::And },
    { TokenType::Or.name, TokenType::Or },

    { TokenType::BitwiseOr.name, TokenType::BitwiseOr },
    { TokenType::BitwiseAnd.name, TokenType::BitwiseAnd },
    { TokenType::BitwiseXor.name, TokenType::BitwiseXor },
    { TokenType::BitwiseNot.name, TokenType::BitwiseNot },
    { TokenType::BitwiseLShift.name, TokenType::BitwiseLShift },
    { TokenType::BitwiseRShift.name, TokenType::BitwiseRShift },

    { TokenType::Compare.name, TokenType::Compare },
    { TokenType::NotCompare.name, TokenType::NotCompare },
    { TokenType::Spaceship.name, TokenType::Spaceship },

    { TokenType::Arrow.name, TokenType::Arrow },

    { TokenType::PlusEquals.name, TokenType::PlusEquals },
    { TokenType::MinusEquals.name, TokenType::MinusEquals },
    { TokenType::MultiplyEquals.name, TokenType::MultiplyEquals },
    { TokenType::DivideEquals.name, TokenType::DivideEquals },
    { TokenType::ModulusEquals.name, TokenType::ModulusEquals },
    { TokenType::BitwiseOrEquals.name, TokenType::BitwiseOrEquals },
    { TokenType::BitwiseAndEquals.name, TokenType::BitwiseAndEquals },
    { TokenType::BitwiseXorEquals.name, TokenType::BitwiseXorEquals },
    { TokenType::BitwiseLShiftEquals.name, TokenType::BitwiseLShiftEquals },
    { TokenType::BitwiseRShiftEquals.name, TokenType::BitwiseRShiftEquals },

    { TokenType::Identifier.name, TokenType::Identifier },
    { TokenType::Number.name, TokenType::Number },
    { TokenType::String.name, TokenType::String },
    { TokenType::Keyword.name, TokenType::Keyword }
};

TokenType* TokenType::getType(std::string value) {
    if (value == "") {
        return nullptr;
    }

    if (TokenType::s_Values.count(value)) {
        return &TokenType::s_Values[value];
    }

    if (isdigit(value[0]) || value[0] == '.') {
        // What?
        if (value.length() > 1) {
            if (value[1] == 'x' or value[1] == 'X') {
                return &TokenType::Number;
            }
        }

        if (value.find('.') != std::string::npos) {
            return &TokenType::Number;
        }
        return &TokenType::Number;
    }
    else if ((value[0] == '"' && value.back() == '"') || (value[0] == '\'' && value.back() == '\'')) {
        return &TokenType::String;
    }

    // Check if string is keyword
    if (Keywords::s_Values.count(value)) {
        return &TokenType::Keyword;
    }

    // Nothing else, must be identifier
    return &TokenType::Identifier;
}

bool TokenType::hasValue(std::string value) {
    return TokenType::s_Values.count(value);
}

LexerToken* LexerToken::NONE = new LexerToken("", &TokenType::NoneToken);
