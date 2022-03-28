#include "parser.h"

NodeArrayExpression* Parser::parseArrayExpression() {
    bool isDictionary = false;
    std::vector<AstNode*> members;
    std::vector<std::vector<AstNode*>> dictionaryMembers = { std::vector<AstNode*>(), std::vector<AstNode*>() };

    // Eat left bracket
    if (this->eat(&TokenType::LBracket) == nullptr) {
        return nullptr;
    }

    LexerToken* token = this->currentToken();

    bool atDictionaryValue = false;

    if (this->peekToken(0, &TokenType::Colon) && this->peekToken(1, &TokenType::RBracket)) {
        isDictionary = true;
        dictionaryMembers = { std::vector<AstNode*>(), std::vector<AstNode*>() };
        this->eat(&TokenType::Colon);
        token = this->currentToken();
    }

    while (token->type != &TokenType::RBracket) {
        // Parse expr
        AstNode* itemExpr = this->parseExpression();

        if (itemExpr == nullptr) {
            this->error(Util::format("invalid array member item %s", this->currentToken()));
            return nullptr;
        }

        if (!isDictionary && members.empty() && this->peekToken(0, &TokenType::Colon)) {
            isDictionary = true;
            dictionaryMembers = { std::vector<AstNode*>(), std::vector<AstNode*>() };
        }

        if (isDictionary) {
            if (!atDictionaryValue) {
                dictionaryMembers[0].push_back(itemExpr);
            }
            else {
                dictionaryMembers[1].push_back(itemExpr);
            }
        }
        else {
            members.push_back(itemExpr);
        }

        if (this->currentToken()->type == &TokenType::Comma) {
            this->eat(&TokenType::Comma);
            if (isDictionary && atDictionaryValue) {
                atDictionaryValue = false;
            }
        }
        else if (this->currentToken()->type == &TokenType::Colon && isDictionary && !atDictionaryValue) {
            this->eat(&TokenType::Colon);
            atDictionaryValue = true;
        }
        else {
            break;
        }
    }

    if (isDictionary) {
        members = { new NodeArrayExpression(dictionaryMembers[0], token), new NodeArrayExpression(dictionaryMembers[1], token) };
    }

    if (this->eat(&TokenType::RBracket) == nullptr) {
        return nullptr;
    }

    return new NodeArrayExpression(members, token, isDictionary);
}

NodeArrayAccessExpression* Parser::parseArrayAccessExpression(AstNode* lhs) {
    if (this->eat(&TokenType::LBracket) == nullptr) {
        return nullptr;
    }

    LexerToken* token = this->currentToken();

    // Get internal expr
    AstNode* accessExpr = this->parseExpression();

    if (accessExpr == nullptr) {
        this->error("invalid array access expression");
        return nullptr;
    }

    if (this->eat(&TokenType::RBracket) == nullptr) {
        return nullptr;
    }

    return new NodeArrayAccessExpression(lhs, accessExpr, token);
}

NodeDeclare* Parser::parseVariableDeclaration(bool requireKeyword) {
    // let VARNAME:TYPE parseAssignmentStatement

    if (requireKeyword) {
        // Eat let keyword
        if (this->eat(&TokenType::Keyword) == nullptr) {
            return nullptr;
        }
    }
    else if (this->peekToken(0, &TokenType::Keyword) && this->peekToken(0)->value == "func") {
        // return this->parseFuncDeclaration();
    }

    LexerToken* name = this->currentToken();
    if (this->eat(&TokenType::Identifier) == nullptr) {
        return nullptr;
    }

    AstNode* typeNode = nullptr;
    bool allowCasting = false;

    // Manual type set
    if (this->currentToken()->type == &TokenType::Colon) {
        this->eat(&TokenType::Colon);
        LexerToken* typeNodeToken = this->currentToken();
        typeNode = this->parseFactor();

        if (typeNode == nullptr || (!Util::isType<NodeVariable*>(typeNode) && !Util::isType<NodeMemberExpression*>(typeNode))) {
            this->error(Util::format("Declaration type should either be an identifier or member access, got %s", Util::toString(typeNodeToken)));
            return nullptr;
        }

        if (this->currentToken()->type == &TokenType::Question) {
            this->eat(&TokenType::Question);
            allowCasting = true;
        }
    }

    AstNode* valNode = nullptr;
    if (this->currentToken()->type == &TokenType::Equals) {
        valNode = this->parseAssignmentStatement(new NodeVariable(name, allowCasting));
    }
    else {
        valNode = new NodeNone(name);
    }

    NodeDeclare* vnodes = new NodeDeclare(typeNode, name, valNode, allowCasting);

    return vnodes;
}

NodeMemberExpression* Parser::parseMemberExpression(AstNode* lhs) {
    if (this->eat(&TokenType::Dot) == nullptr) {
        return nullptr;
    }

    LexerToken* token = this->currentToken();

    // Expect identifier for right hand side
    LexerToken* rhsName = this->peekToken(0, &TokenType::Identifier);

    if (rhsName == nullptr) {
        this->error("invalid member access: must be in format <expression>.<identifier>");
        return nullptr;
    }

    this->eat(&TokenType::Identifier);

    return new NodeMemberExpression(lhs, rhsName, token);
}

NodeObjectExpression* Parser::parseObjectExpression() {
    std::vector<NodeDeclare*> members = {}; // Array of var declarations

    // Eat left brace
    if (this->eat(&TokenType::LBrace) == nullptr) {
        return nullptr;
    }

    LexerToken* token = this->currentToken();

    // Find all lines in block
    while (token->type != &TokenType::RBrace) {
        // Parse variable declaration
        NodeDeclare* varDecl = this->parseVariableDeclaration(false);

        if (varDecl == nullptr) {
            this->error("invalid object member declaration");
            return nullptr;
        }

        members.push_back(varDecl);

        token = this->currentToken();
    }

    if (this->eat(&TokenType::RBrace) == nullptr) {
        return nullptr;
    }

    return new NodeObjectExpression(members);
}

// Parse reference to a variable
NodeVariable* Parser::parseVariable() {
    // Create variable node && eat identifier
    NodeVariable* variableNode = new NodeVariable(this->currentToken());

    this->eat(&TokenType::Identifier);

    return variableNode;
}

AstNode* Parser::parseExpression() {
    AstNode* node = this->parseTerm();

    std::vector<TokenType*> multiopTypes = {
        &TokenType::PlusEquals, &TokenType::MinusEquals,
        &TokenType::MultiplyEquals, &TokenType::DivideEquals,
        &TokenType::ModulusEquals,
        &TokenType::BitwiseOrEquals, &TokenType::BitwiseAndEquals,
        &TokenType::BitwiseXorEquals,
        &TokenType::BitwiseLShiftEquals, &TokenType::BitwiseRShiftEquals
    };

    std::vector<TokenType*> expectedTypes = {
        &TokenType::Equals,
        &TokenType::Plus, &TokenType::Minus, &TokenType::Modulus,
        &TokenType::Compare, &TokenType::NotCompare,
        &TokenType::Spaceship,
        &TokenType::Arrow,
        &TokenType::LessThan, &TokenType::GreaterThan,
        &TokenType::LessThanEqual, &TokenType::GreaterThanEqual,
        &TokenType::BitwiseOr, &TokenType::BitwiseAnd, &TokenType::BitwiseXor,
        &TokenType::And, &TokenType::Or,
        &TokenType::BitwiseLShift, &TokenType::BitwiseRShift,
        &TokenType::Exponentiation
    };
    expectedTypes.insert(expectedTypes.end(), multiopTypes.begin(), multiopTypes.end());

    while (std::find(expectedTypes.begin(), expectedTypes.end(), this->currentToken()->type) != expectedTypes.end()) {
        LexerToken* token = this->currentToken();

        if (this->peekToken(0, &TokenType::Equals)) {
            node = this->parseAssignmentStatement(node);
            continue;
        }

        if (std::find(multiopTypes.begin(), multiopTypes.end(), this->currentToken()->type) != multiopTypes.end()) {
            // Parse (lhs [operator] rhs) && return assign node
            NodeAssign* assignNode = this->parseAssignmentStatement(node);

            // This is slightly sketchy, but also will be able to handle
            // operations like <<= && any other multichar operation
            LexerToken* operation = new LexerToken(Util::trimCopy(token->value, "="));

            // Make value (lhs [operator] rhs)
            NodeBinOp* valueNode = new NodeBinOp(node, operation, assignNode->value);

            // Final node should be (lhs [=] lhs [operator] rhs)
            assignNode->value = valueNode;
            node = assignNode;
            continue;
        }

        if (std::find(expectedTypes.begin(), expectedTypes.end(), token->type) != expectedTypes.end()) {
            this->eat();
        }

        if ((token->type == &TokenType::Or || token->type == &TokenType::And) && std::find(expectedTypes.begin(), expectedTypes.end(), this->peekToken()->type) != expectedTypes.end()) {
            node = new NodeBinOp(node, token, this->parseExpression());
            continue;
        }

        node = new NodeBinOp(node, token, this->parseTerm());
    }
    return node;
}

AstNode* Parser::parseTerm() {
    // Handles multiply, division, expressions
    AstNode* node = this->parseFactor();
    while (this->currentToken()->type == &TokenType::Multiply || this->currentToken()->type == &TokenType::Divide) {
        LexerToken* token = this->currentToken();
        if (token->type == &TokenType::Multiply) {
            this->eat(&TokenType::Multiply);
        }
        else if (token->type == &TokenType::Divide) {
            this->eat(&TokenType::Divide);
        }
        node = new NodeBinOp(node, token, this->parseFactor());
    }
    return node;
}
