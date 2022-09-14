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
    NodeIfStatement* parseIfStatement();
    NodeDeclare* parseFuncDeclaration();
    NodeImport* importFile(std::string filename, LexerToken* filenameToken = nullptr);
    NodeImport* parseImport();
    NodeFunctionReturn* parseReturn();
    NodeWhile* parseWhile();
    NodeFor* parseFor();
    NodeDeclare* parseMacro();
    NodeMixin* parseMixin();
    NodeTryCatch* parseTry();
    
    std::vector<LexerToken*> tokens;
    int tokenIndex;
    LexerToken* m_CurrentToken;
    ErrorList errorList;

    SourceLocation sourceLocation;

    //Parser() = default;
    Parser() {}
    Parser(std::vector<LexerToken*> tokens, SourceLocation sourceLocation) {
        this->tokens = tokens;
        this->tokenIndex = 0;
        this->m_CurrentToken = this->nextToken();
        this->errorList = ErrorList();

        this->sourceLocation = sourceLocation;
    }
    Parser(std::vector<LexerToken*> tokens, SourceLocation* sourceLocation) {
        this->tokens = tokens;
        this->tokenIndex = 0;
        this->m_CurrentToken = this->nextToken();
        this->errorList = ErrorList();

        this->sourceLocation = *sourceLocation;
    }

    AstNode* call(std::string name) {
        if (name == "let") {
            return this->parseVariableDeclaration();
        }
        else if (name == "if") {
            return this->parseIfStatement();
        }
        else if (name == "func") {
            return this->parseFuncDeclaration();
        }
        else if (name == "import") {
            return this->parseImport();
        }
        else if (name == "return") {
            return this->parseReturn();
        }
        else if (name == "while") {
            return this->parseWhile();
        }
        else if (name == "for") {
            return this->parseFor();
        }
        else if (name == "macro") {
            return this->parseMacro();
        }
        else if (name == "mixin") {
            return this->parseMixin();
        }
        else if (name == "try") {
            return this->parseTry();
        }
        return nullptr;
    }

    std::string filename() {
        return this->sourceLocation.filename;
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
        Error error = Error(ErrorType::Syntax, this->currentToken()->location, message, this->filename(), "Syntax Error");
        this->errorList.pushError(error);
    }

    // Read next token and error if token->type != passed in token type
    LexerToken* eat(TokenType* tokenType = nullptr) {
        if (tokenType != nullptr) {
            if (this->expectToken(tokenType) == nullptr) {
                return nullptr;
            }
        }

        this->m_CurrentToken = this->nextToken();

        return this->currentToken();
    }

    AstNode* parseKeyword() {
        LexerToken* keyword = this->expectToken(&TokenType::Keyword);
        
        AstNode* result = this->call(keyword->value);
        if (result == nullptr) {
            this->error(Util::format("%s is not a valid keyword", keyword));
        }

        return result;
    }
    
    AstNode* parseStatement() {
        LexerToken* token = this->currentToken();

        if (token->type == &TokenType::NoneToken) {
            throw std::runtime_error("none");
        }
        
        // Empty statement, eat semicolon and try again
        if (token->type == &TokenType::Semicolon) {
            this->eat(&TokenType::Semicolon);
            return new NodeNone(token);
        }
            
        AstNode* node;
        if (token->type == &TokenType::Keyword) {
            node = this->parseKeyword();

            if (node == nullptr) {
                return nullptr;
            }
            
            // Check if node is function block, exempt from semicolon
            if (node->type == &NodeType::Declare && (!((NodeDeclare*) node)->value.empty() && boost::any_cast<AstNode*>(((NodeDeclare*) node)->value)->type == &NodeType::Assign)) {
                NodeAssign* a = boost::any_cast<NodeAssign*>(((NodeDeclare*) node)->value);
                AstNode* rhs = boost::any_cast<AstNode*>(a->value);
                if (rhs->type == &NodeType::FunctionExpression || rhs->type == &NodeType::Macro) {
                    return node;
                }
            }
            
            if (node->type == &NodeType::IfStatement || node->type == &NodeType::Try || node->type == &NodeType::While || node->type == &NodeType::For || node->type == &NodeType::Mixin) {
                return node;
            }
        }
        else {
            node = this->parseExpression();
            
            if (node == nullptr) {
                this->error(Util::format("Unknown token %s in statement", Util::toString(token->type).c_str()));
                node = nullptr;
            }
        }
        
        if (this->currentToken()->type != &TokenType::Semicolon) {
            this->error(Util::format("Missing semicolon (found %s)", this->currentToken()->type->name.c_str()));
        }
        else {
            // Eat semicolon at end of statement
            this->eat(&TokenType::Semicolon);
        }

        return node;
    }

    std::vector<AstNode*> getStatements() {
        std::vector<AstNode*> statements = {};
        
        // Read until no statements left
        while (this->currentToken() != LexerToken::NONE) {
            // We hit last statement in block, break
            if (this->currentToken()->type == &TokenType::RBrace) {
                break;
            }
                
            AstNode* statement = this->parseStatement();
            // Parse statement and skip to next semicolon
            statements.push_back(statement);
        }

        return statements;
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

    NodeArgumentList* parseArgumentList() {
        // Eat open parenthesis
        if (this->eat(&TokenType::LParen) == nullptr) {
            return nullptr;
        }

        NodeArgumentList* argumentList = nullptr;

        if (this->peekToken(0, &TokenType::RParen)) {
            argumentList = new NodeArgumentList({}, this->currentToken());
        }
        else {
            std::deque<AstNode*> arguments = {};
            bool hasVargs = false;
            bool firstArg = true;

            bool anyDefault = false;

            while (true) {
                if (hasVargs) {
                    this->error("Arguments provided after variadic arguments");
                    break;
                }

                bool isVargs = false;

                if (this->peekToken(0, &TokenType::Multiply)) {
                    isVargs = true;
                    hasVargs = true;
                }

                AstNode* argument = nullptr;

                if (isVargs) {
                    // Eat *
                    if (this->eat(&TokenType::Multiply) == nullptr) {
                        return nullptr;
                    }

                    LexerToken* token = this->currentToken();
                    NodeVariable* var = this->parseVariable();

                    if (var == nullptr) {
                        return nullptr;
                    }

                    argument = new NodeSplatArgument(var, token);
                }
                else {
                    if (this->expectToken(&TokenType::Identifier) == nullptr) {
                        this->error("invalid argument format");
                        break;
                    }

                    // Parse declaration(vname:type) without let keyword
                    argument = this->parseVariableDeclaration(false);
                }
                if (argument == nullptr) {
                    this->error("invalid argument");
                    break;
                }
                bool anyDefault = false;
                if (!Util::isType<NodeSplatArgument>(argument) && (boost::any_cast<AstNode*>(boost::any_cast<NodeDeclare*>(argument)->value)->hasValue())) {
                    anyDefault = true;
                }
                else {
                    if (anyDefault) {
                        this->error("non-default argument follows default argument");
                        break;
                    }
                }

                arguments.push_back(argument);

                bool firstArg = true;
                if (this->peekToken(0, &TokenType::Comma)) {
                    // Eat comma and continue on with argument list
                    this->eat(&TokenType::Comma);

                    firstArg = false;
                }
                else if (!firstArg && !this->peekToken(0, &TokenType::RParen) && !this->peekToken(1, &TokenType::LBrace)) {
                    // Not first arg and no comma, rollback?
                    break;
                }
                else {
                    break;
                }
            }

            argumentList = new NodeArgumentList(arguments, this->currentToken());
        }
        
        if (argumentList == nullptr) {
            this->error("invalid argument list");
            return nullptr;
        }
        
        // Eat closing parenthesis
        this->eat(&TokenType::RParen);
            
        return argumentList;
    }

    NodeBlock* parseBlockStatement() {
        this->eat(&TokenType::LBrace);
        NodeBlock* block = new NodeBlock(this->currentToken());
        block->children = this->getStatements();
        this->eat(&TokenType::RBrace);

        return block;
    }
    
    NodeFunctionExpression* parseArrowFunction(AstNode* node) {
        LexerToken* token = this->currentToken();
    
        std::deque<AstNode*> arguments = {};

        if (Util::isType<NodeVariable>(node)) {
            arguments.push_back(new NodeDeclare(nullptr, boost::any_cast<LexerToken>(node->token), new NodeNone(token)));
        }

        if (this->eat(&TokenType::Arrow) == nullptr) {
            return nullptr;
        }

        AstNode* expr = this->parseExpression();

        NodeFunctionReturn* returnNode = new NodeFunctionReturn(expr, token);

        NodeBlock* block = new NodeBlock(token);
        block->children = { returnNode };

        NodeFunctionExpression* funExpr = new NodeFunctionExpression(
            new NodeArgumentList(
                arguments,
                token
            ),
            block
        );

        return funExpr;
    }

    NodeFunctionExpression* parseFunctionExpression() {
        LexerToken* token = this->currentToken();
        if (this->eat(&TokenType::Keyword) == nullptr) {
            return nullptr;
        }

        NodeArgumentList* argumentList = this->parseArgumentList();

        if (argumentList == nullptr) {
            return nullptr;
        }

        NodeBlock* block = this->parseBlockStatement();

        if (block == nullptr) {
            return nullptr;
        }

        return new NodeFunctionExpression(argumentList, block);
    }

    AstNode* parseFunctionCall(AstNode* node) {
        this->eat(&TokenType::LParen);
        
        std::deque<AstNode*> argnames = {};
        LexerToken* last = this->currentToken();
        
        if (this->currentToken()->type != &TokenType::RParen) {
            // Skip until RParen
            while (this->currentToken()->type != &TokenType::RParen) {
                // Append argument to ArgumentList node
                if (this->peekToken(0, &TokenType::Multiply)) {
                    // Splat args
                    LexerToken* vargsToken = this->currentToken();
                    this->eat(&TokenType::Multiply);
                    AstNode* splatExpr = this->parseExpression();

                    if (splatExpr == nullptr) {
                        return nullptr;
                    }

                    argnames.push_back(new NodeSplatArgument(splatExpr, vargsToken));
                }
                else {
                    argnames.push_back(this->parseExpression());
                }

                if (this->currentToken()->type == &TokenType::RParen) {
                    break;
                }

                this->eat();

                if (this->currentToken()->type == &TokenType::NoneToken) {
                    return new NodeNone(last);
                }
            }
        }
        
        // Eat closing paren
        this->eat(&TokenType::RParen);

        NodeArgumentList* args = new NodeArgumentList(argnames, this->currentToken());
        
        return new NodeCall(node, args);
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
                node = this->parseArrowFunction(node);
            }
        }
        else if (token->type == &TokenType::Keyword) {
            if (new Keywords(token->value) == &Keywords::Func) {
                node = this->parseFunctionExpression();
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
                node = this->parseFunctionCall(node);
            }
        }

        return node;
    }

    std::vector<AstNode*> parse() {
        return this->getStatements();
    }
};
