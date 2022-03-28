#pragma once

#include "lexer.h"
#include "error.h"
#include "source_location.h"
#include "node.h"

class Parser {
public:
    NodeArrayExpression* parseArrayExpression();
    NodeArrayAccessExpression* parseArrayAccessExpression(AstNode* lhs);
    NodeDeclare* parseVariableDeclaration(bool requireKeyword = true);
    NodeMemberExpression* parseMemberExpression(AstNode* lhs);
    NodeObjectExpression* parseObjectExpression();
    NodeVariable* parseVariable();
    AstNode* parseExpression();
    AstNode* parseTerm();
    
    std::vector<LexerToken*> tokens;
    int tokenIndex;
    LexerToken* m_CurrentToken;
    ErrorList* errorList;

    SourceLocation* sourceLocation;

    typedef AstNode* (Parser::*Action)(AstNode*);
    std::map<std::string, Action> keywordMethods;

    Parser() = default;
    Parser(std::vector<LexerToken*> tokens, SourceLocation* sourceLocation) {
        this->tokens = tokens;
        this->tokenIndex = 0;
        this->m_CurrentToken = this->nextToken();
        this->errorList = new ErrorList();

        this->sourceLocation = sourceLocation;

        this->keywordMethods = {
            // { "let", &Parser::parseVariableDeclaration }
            // { "if", &Parser::parseIfStatement },
            // { "func", &Parser::parseFuncDeclaration },
            // { "import", &Parser::parseImport },
            // { "return", &Parser::parseReturn },
            // { "while", &Parser::parseWhile },
            // { "for", &Parser::parseFor },
            // { "macro", &Parser::parseMacro },
            // { "mixin", &Parser::parseMixin },
            // { "try", &Parser::parseTry }
        };
        this->keywordMethods["let"] = &Parser::parseVariableDeclaration;
    }

    std::string filename() {
        return this->sourceLocation->filename;
    }

    LexerToken* currentToken() {
        if (this->m_CurrentToken == nullptr) {
            return LexerToken::NONE;
        }

        return this->m_CurrentToken;
    }

    LexerToken* expectToken(TokenType* tokenType, int offset = 0, LexerToken* token = nullptr) {
        // If no token passed in, peek from offset
        if (token == nullptr) {
            token = this->peekToken(offset);
        }

        if (token->type == tokenType) {
            return token;
        }
        else {
            this->error(Util::format("expected %s but recieved %s", tokenType->name.c_str(), token->type->name.c_str()));
            return nullptr;
        }
    }

    LexerToken* nextToken() {
        // Check if next index is past list boundaries
        if (this->tokenIndex+1 > this->tokens.size()) {
            return nullptr;
        }

        // Return selected token, increment index
        this->m_CurrentToken = this->tokens[this->tokenIndex];
        this->tokenIndex += 1;

        return this->currentToken();
    }

    // Return token at token->index + offset
    LexerToken* peekToken(int offset = 1, TokenType* expectedType = nullptr) {
        // Check bounds
        if (this->tokenIndex+offset-1 > this->tokens.size()) {
            return nullptr;
        }

        LexerToken* token = this->tokens[this->tokenIndex+offset-1];

        // Check type if expectedType != nullptr
        if (expectedType != nullptr && token->type != expectedType) {
            return nullptr;
        }

        return token;
    }

    void error(std::string message) {
        // Tokens have locations attached from the lexer, pass to this->error
        // if an error occurs
        Error* error = new Error(ErrorType::Syntax, this->currentToken()->location, message, this->filename(), "Syntax Error");
        this->errorList->pushError(error);
    }

    // Read next token and error if token.type != passed in token type
    LexerToken* eat(TokenType* tokenType = nullptr) {
        if (tokenType != nullptr) {
            if (this->expectToken(tokenType) == nullptr) {
                return nullptr;
            }
        }

        this->m_CurrentToken = this->nextToken();

        return this->currentToken();
    }

    NodeAssign* parseAssignmentStatement(AstNode* _node, bool requireOperator = true) {
        // Operator would be '=' or '+=', '-=', etc.
        if (requireOperator) {
            this->eat();
        }

        AstNode* value = this->parseExpression();

        if (value == nullptr) {
            this->error("Invalid assignment");
            return nullptr;
        }

        NodeAssign* node = new NodeAssign(_node, value);

        return node;
    }

    AstNode* parseFactor() {
        // Handles value or (x ± x)
        LexerToken* token = this->currentToken();

        AstNode* node = nullptr;

        // Handle +, -
        if (token->type == &TokenType::Plus || token->type == &TokenType::Minus) {
            this->eat(token->type);
            node = new NodeUnaryOp(token, this->parseFactor());
        }

        // Handle '!'
        else if (token->type == &TokenType::Not) {
            this->eat(&TokenType::Not);
            node = new NodeUnaryOp(token, this->parseFactor());
        }

        // Handle '~'
        else if (token->type == &TokenType::BitwiseNot) {
            this->eat(&TokenType::BitwiseNot);
            node = new NodeUnaryOp(token, this->parseFactor());
        }

        else if (token->type == &TokenType::Number) {
            this->eat(&TokenType::Number);
            node = new NodeNumber(token);
        }

        else if (token->type == &TokenType::String) {
            this->eat(&TokenType::String);
            node = new NodeString(token);
        }

        else if (token->type == &TokenType::LParen) {
            this->eat(&TokenType::LParen);
            node = this->parseExpression();
            this->eat(&TokenType::RParen);
        }
        else if (token->type == &TokenType::LBracket) {
            node = this->parseArrayExpression();
        }
        else if (token->type == &TokenType::LBrace) {
            node = this->parseObjectExpression();
        }
        else if (token->type == &TokenType::Identifier) {
            node = this->parseVariable();

            if (this->peekToken(0, &TokenType::Arrow)) {
                // node = this->parseArrowFunction(node);
            }
        }
        else if (token->type == &TokenType::Keyword) {
            if (new Keywords(token->value) == &Keywords::Func) {
                // node = this->parseFunctionExpression();
            }
            else {
                this->error(Util::format("Invalid usage of keyword %s in expression", token->value));
                return nullptr;
            }
        }

        if (node == nullptr) {
            this->error(Util::format("Unexpected token: %s", this->currentToken()));
            this->eat();
            return nullptr;
        }

        while (this->currentToken()->type == &TokenType::Dot || this->currentToken()->type == &TokenType::LParen || this->currentToken()->type == &TokenType::LBracket) {
            if (this->peekToken(0, &TokenType::Dot)) {
                node = this->parseMemberExpression(node);
            }
            else if (this->peekToken(0, &TokenType::LBracket)) {
                node = this->parseArrayAccessExpression(node);
            }
            else if (this->peekToken(0, &TokenType::LParen)) {
                // node = this->parseFunctionCall(node);
            }
        }

        return node;
    }
};
