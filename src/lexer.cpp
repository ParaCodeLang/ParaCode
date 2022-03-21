#include "lexer.h"

boost::any Keywords::Let = "let";
boost::any Keywords::If = "if";
boost::any Keywords::Else = "else";
boost::any Keywords::Elif = "elif";
boost::any Keywords::Func = "func";
boost::any Keywords::Import = "import";
boost::any Keywords::Return = "return";
boost::any Keywords::While = "while";
boost::any Keywords::For = "for";
boost::any Keywords::In = "in";
boost::any Keywords::Macro = "macro";
boost::any Keywords::Mixin = "mixin";
boost::any Keywords::Try = "try";
boost::any Keywords::Catch = "catch";
boost::any Keywords::Finally = "finally";

std::map<std::string, boost::any> Keywords::s_Values = {
    { "Let", Keywords::Let },
    { "If", Keywords::If },
    { "Else", Keywords::Else },
    { "Elif", Keywords::Elif },
    { "Func", Keywords::Func },
    { "Import", Keywords::Import },
    { "Return", Keywords::Return },
    { "While", Keywords::While },
    { "For", Keywords::For },
    { "In", Keywords::In },
    { "Macro", Keywords::Macro },
    { "Mixin", Keywords::Mixin },
    { "Try", Keywords::Try },
    { "Catch", Keywords::Catch },
    { "Finally", Keywords::Finally }
};


boost::any TokenType::NoneToken = 1;

boost::any TokenType::LParen = "(";
boost::any TokenType::RParen = ")";
boost::any TokenType::LBrace = "{";
boost::any TokenType::RBrace = "}";
boost::any TokenType::LBracket = "[";
boost::any TokenType::RBracket = "]";
boost::any TokenType::Plus = "+";
boost::any TokenType::Minus = "-";
boost::any TokenType::Multiply = "*";
boost::any TokenType::Exponentiation = "**";
boost::any TokenType::Divide = "/";
boost::any TokenType::Equals = "=";
boost::any TokenType::Semicolon = ";";
boost::any TokenType::Colon = ":";
boost::any TokenType::Dot = ".";
boost::any TokenType::Comma = ",";
boost::any TokenType::Not = "!";
boost::any TokenType::Question = "?";
boost::any TokenType::Modulus = "%";
boost::any TokenType::LessThan = "<";
boost::any TokenType::LessThanEqual = "<=";
boost::any TokenType::GreaterThan = ">";
boost::any TokenType::GreaterThanEqual = ">=";

boost::any TokenType::And = "&&";
boost::any TokenType::Or = "||";

boost::any TokenType::BitwiseOr = "|";
boost::any TokenType::BitwiseAnd = "&";
boost::any TokenType::BitwiseXor = "^";
boost::any TokenType::BitwiseNot = "~";
boost::any TokenType::BitwiseLShift = "<<";
boost::any TokenType::BitwiseRShift = ">>";

boost::any TokenType::Compare = "==";
boost::any TokenType::NotCompare = "!=";
boost::any TokenType::Spaceship = "<=>";

boost::any TokenType::Arrow = "->";

boost::any TokenType::PlusEquals = "+=";
boost::any TokenType::MinusEquals = "-=";
boost::any TokenType::MultiplyEquals = "*=";
boost::any TokenType::DivideEquals = "/=";
boost::any TokenType::ModulusEquals = "%=";
boost::any TokenType::BitwiseOrEquals = "|=";
boost::any TokenType::BitwiseAndEquals = "&=";
boost::any TokenType::BitwiseXorEquals = "^=";
boost::any TokenType::BitwiseLShiftEquals = "<<=";
boost::any TokenType::BitwiseRShiftEquals = ">>=";

boost::any TokenType::Identifier = 2;
boost::any TokenType::Number = 3;
boost::any TokenType::String = 4;
boost::any TokenType::Keyword = 5;

std::map<std::string, boost::any> TokenType::s_Values = {
    { "NoneToken", TokenType::NoneToken },

    { "LParen", TokenType::LParen },
    { "RParen", TokenType::RParen },
    { "LBrace", TokenType::LBrace },
    { "RBrace", TokenType::RBrace },
    { "LBracket", TokenType::LBracket },
    { "RBracket", TokenType::RBracket },
    { "Plus", TokenType::Plus },
    { "Minus", TokenType::Minus },
    { "Multiply", TokenType::Multiply },
    { "Exponentiation", TokenType::Exponentiation },
    { "Divide", TokenType::Divide },
    { "Equals", TokenType::Equals },
    { "Semicolon", TokenType::Semicolon },
    { "Colon", TokenType::Colon },
    { "Dot", TokenType::Dot },
    { "Comma", TokenType::Comma },
    { "Not", TokenType::Not },
    { "Question", TokenType::Question },
    { "Modulus", TokenType::Modulus },
    { "LessThan", TokenType::LessThan },
    { "LessThanEqual", TokenType::LessThanEqual },
    { "GreaterThan", TokenType::GreaterThan },
    { "GreaterThanEqual", TokenType::GreaterThanEqual },

    { "And", TokenType::And },
    { "Or", TokenType::Or },

    { "BitwiseOr", TokenType::BitwiseOr },
    { "BitwiseAnd", TokenType::BitwiseAnd },
    { "BitwiseXor", TokenType::BitwiseXor },
    { "BitwiseNot", TokenType::BitwiseNot },
    { "BitwiseLShift", TokenType::BitwiseLShift },
    { "BitwiseRShift", TokenType::BitwiseRShift },

    { "Compare", TokenType::Compare },
    { "NotCompare", TokenType::NotCompare },
    { "Spaceship", TokenType::Spaceship },

    { "Arrow", TokenType::Arrow },

    { "PlusEquals", TokenType::PlusEquals },
    { "MinusEquals", TokenType::MinusEquals },
    { "MultiplyEquals", TokenType::MultiplyEquals },
    { "DivideEquals", TokenType::DivideEquals },
    { "ModulusEquals", TokenType::ModulusEquals },
    { "BitwiseOrEquals", TokenType::BitwiseOrEquals },
    { "BitwiseAndEquals", TokenType::BitwiseAndEquals },
    { "BitwiseXorEquals", TokenType::BitwiseXorEquals },
    { "BitwiseLShiftEquals", TokenType::BitwiseLShiftEquals },
    { "BitwiseRShiftEquals", TokenType::BitwiseRShiftEquals },

    { "Identifier", TokenType::Identifier },
    { "Number", TokenType::Number },
    { "String", TokenType::String },
    { "Keyword", TokenType::Keyword }
};
