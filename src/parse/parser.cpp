#include "parser.h"

#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/algorithm/string/predicate.hpp>

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
        return this->parseFuncDeclaration();
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

        if (typeNode == nullptr || (!Util::isType<NodeVariable>(typeNode) && !Util::isType<NodeMemberExpression>(typeNode))) {
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

NodeIfStatement* Parser::parseIfStatement() {
    // Eat `if`
    LexerToken* ifToken = this->currentToken();
    if (this->eat(&TokenType::Keyword) == nullptr) {
        return nullptr;
    }

    AstNode* expr = this->parseExpression();

    if (expr == nullptr) {
        return nullptr;
    }

    NodeBlock* block = this->parseBlockStatement();

    if (block == nullptr) {
        return nullptr;
    }

    AstNode* elseBlock = nullptr;
    
    LexerToken* token = this->currentToken();

    if (token->type == &TokenType::Keyword) {
        if (new Keywords(token->value) == &Keywords::Else) {
            // Eat else
            this->eat(&TokenType::Keyword);
            elseBlock = this->parseBlockStatement();
        }
        else if (new Keywords(token->value) == &Keywords::Elif) {
            elseBlock = this->parseIfStatement();
        }
    }

    return new NodeIfStatement(expr, block, elseBlock, ifToken);
}

NodeDeclare* Parser::parseFuncDeclaration() {
    // func NAME(...) { ... }
    
    // Eat func keyword
    LexerToken* type = this->currentToken();
    this->eat(&TokenType::Keyword);
    // Eat function name
    LexerToken* name = this->currentToken();
    if (this->eat(&TokenType::Identifier) == nullptr) {
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

    NodeFunctionExpression* funExpr = new NodeFunctionExpression(argumentList, block);
    
    // Parse assignment, parenthesis, etc.
    NodeAssign* valNode = new NodeAssign(new NodeVariable(name), funExpr);
    NodeVariable* typeNode = new NodeVariable(new LexerToken("Func", &TokenType::Identifier));
    NodeDeclare* node = new NodeDeclare(typeNode, name, valNode);
    
    return node;
}

NodeImport* Parser::importFile(std::string filename, LexerToken* filenameToken) {
    std::string data;
    try {
        data = Util::readFile(filename);
        if (!boost::algorithm::ends_with(filename, ".para") && !boost::algorithm::ends_with(filename, ".paracode")) {
            this->error(Util::format("source file '%s's file extension ('.%s') is not a valid ParaCode extension", filename.c_str(), Util::getExtension(filename).c_str()));
            return nullptr;
        }
    }
    catch (std::ifstream::failure &readErr) {
        this->error(Util::format("source file '%s' does not exist", filename.c_str()));
        return nullptr;
    }
    
    // Lex loaded file data
    SourceLocation sourceLocation = SourceLocation(filename);

    Lexer lexer = Lexer(data, sourceLocation);
    std::vector<LexerToken*> tokens = lexer.lex();
    
    Parser parser = Parser(tokens, sourceLocation);
    
    // An import node acts similar to a block and holds all variables and functions
    // in a tree. A parser is passed for getting various information in the interpreter
    if (filenameToken == nullptr) {
        filenameToken = new LexerToken(Util::format("\"%s\"", filename.c_str()));
    }
    
    NodeImport* node = new NodeImport(filenameToken, sourceLocation);
    node->children = parser.getStatements();

    for (auto& error : parser.errorList.errors) {
        this->errorList.pushError(error);
    }
    
    return node;
}

NodeImport* Parser::parseImport() {
    this->eat(&TokenType::Keyword);
    
    std::string filename = "";
    LexerToken* filenameToken = this->currentToken();
    
    // Check for path after import
    this->expectToken(&TokenType::String, 0, filenameToken);
    
    // Trim off ""
    filename = this->currentToken()->value;
    filename = filename.substr(1, filename.size() - 2);
    if (!boost::filesystem::exists(filename)) {
        if (boost::filesystem::exists("pkg_data/" + filename)) {
            filename = "pkg_data/" + filename;
        }
    }
    this->eat(&TokenType::String);
    return this->importFile(filename, filenameToken);
}

NodeFunctionReturn* Parser::parseReturn() {
    this->eat(&TokenType::Keyword);
    AstNode* valueNode = this->parseExpression();
    return new NodeFunctionReturn(valueNode, this->currentToken());
}

NodeWhile* Parser::parseWhile() {
    // Eat while keyword
    LexerToken* token = this->currentToken();
    if (!this->eat(&TokenType::Keyword)) {
        return nullptr;
    }

    AstNode* expression = this->parseExpression();

    if (expression == nullptr) {
        return nullptr;
    }

    NodeBlock* block = this->parseBlockStatement();

    if (block == nullptr) {
        return nullptr;
    }
    
    return new NodeWhile(expression, block, token);
}

NodeFor* Parser::parseFor() {
    // Eat for keyword
    LexerToken* token = this->currentToken();
    if (!this->eat(&TokenType::Keyword)) {
        return nullptr;
    }

    // Get var name of iter
    LexerToken* varToken = this->currentToken();
    this->eat(&TokenType::Identifier);
    if (varToken == nullptr) {
        return nullptr;
    }

    // Eat in keyword
    LexerToken* inKeyword = this->currentToken();
    this->eat(&TokenType::Keyword);
    if (inKeyword == nullptr || inKeyword->value != "in") {
        this->error("for loop expects syntax `for <var> in <expr> { ... }`");
        return nullptr;
    }

    AstNode* expression = this->parseExpression();
    if (expression == nullptr) {
        return nullptr;
    }

    NodeBlock* block = this->parseBlockStatement();

    if (block == nullptr) {
        return nullptr;
    }

    return new NodeFor(varToken, expression, block, token);
}

NodeDeclare* Parser::parseMacro() {
    LexerToken* token = this->currentToken();
    this->eat(&TokenType::Keyword);

    // Eat macro name
    LexerToken* name = this->currentToken();
    if (this->eat(&TokenType::Identifier) == nullptr) {
        return nullptr;
    }

    NodeArgumentList* argumentList = nullptr;

    // Eat optional arguments
    if (this->peekToken(0, &TokenType::LParen)) {
        argumentList = this->parseArgumentList();

        if (argumentList == nullptr) {
            return nullptr;
        }
    }

    // Parse block
    NodeBlock* block = this->parseBlockStatement();
    if (block == nullptr) {
        return nullptr;
    }

    // Add self argument
    NodeDeclare* macroSelfArgument = new NodeDeclare(nullptr, new LexerToken("__macro_self", &TokenType::Identifier), new NodeNone(token));

    if (argumentList == nullptr) {
        argumentList = new NodeArgumentList(
            {macroSelfArgument},
            token
        );
    }
    else {
        argumentList->arguments.push_front(macroSelfArgument);
    }

    NodeFunctionExpression* funExpr = new NodeFunctionExpression(argumentList, block);
    //NodeMacro* macroExpr = new NodeMacro(funExpr, token);

    NodeVariable* macroVar = new NodeVariable(new LexerToken("Macro", &TokenType::Identifier));

    NodeCall* memberAccessCallNode = new NodeCall(
        new NodeMemberExpression(
            macroVar,
            new LexerToken("new", &TokenType::Identifier),
            macroVar->token
        ),
        new NodeArgumentList(
            {funExpr},
            macroVar->token
        )
    );
    
    // Parse assignment, parenthesis, etc.
    NodeAssign* valNode = new NodeAssign(new NodeVariable(name), new NodeMacro(memberAccessCallNode, token));
    NodeVariable* typeNode = new NodeVariable(new LexerToken("Macro", &TokenType::Identifier));
    NodeDeclare* node = new NodeDeclare(typeNode, name, valNode);
    
    return node;
}

NodeMixin* Parser::parseMixin() {
    // TODO: Error if not in macro
    // Eat keyword
    LexerToken* token = this->currentToken();
    this->eat(&TokenType::Keyword);

    // Eat tokens in block
    if (this->eat(&TokenType::LBrace) == nullptr) {
        return nullptr;
    }

    std::vector<LexerToken*> tokens = {};

    int braceLevel = 1;

    while (braceLevel > 0 && this->currentToken() != LexerToken::NONE) {
        if (this->currentToken()->type == &TokenType::LBrace) {
            braceLevel += 1;
        }
        else if (this->currentToken()->type == &TokenType::RBrace) {
            braceLevel -= 1;
        }

        tokens.push_back(this->currentToken());

        this->eat();
    }

    return new NodeMixin(tokens, token);
}

NodeTryCatch* Parser::parseTry() {
    // Eat `try`
    LexerToken* tryToken = this->currentToken();
    if (this->eat(&TokenType::Keyword) == nullptr) {
        return nullptr;
    }

    NodeBlock* block = this->parseBlockStatement();

    if (block == nullptr) {
        return nullptr;
    }

    std::vector<NodeBlock*> catchBlock = {};
    
    LexerToken* token = this->currentToken();
    std::vector<boost::any> expr = {};
    std::vector<NodeDeclare*> variable = {};

    NodeBlock* elseBlock = nullptr;
    NodeBlock* finallyBlock = nullptr;

    while (token->type == &TokenType::Keyword && new Keywords(token->value) == &Keywords::Catch) {
        // Eat catch
        this->eat(&TokenType::Keyword);

        if (this->currentToken()->type == &TokenType::LBracket) {
            std::vector<NodeString*> values = {};
            while (this->currentToken()->type != &TokenType::RBracket) {
                if (this->currentToken()->type != &TokenType::Comma && this->currentToken()->type != &TokenType::LBracket) {
                    values.push_back(new NodeString(this->currentToken()));
                }
                this->eat(this->currentToken()->type);
            }
            this->eat(this->currentToken()->type);
            expr.push_back(values);

            if (this->currentToken()->type == &TokenType::Identifier) {
                AstNode* e = this->parseExpression();
            }
        }
        else if (this->currentToken()->type == &TokenType::LBrace) {
            expr.push_back(new NodeString(new LexerToken("Exception")));
        }
        else if (this->currentToken()->type == &TokenType::Identifier) {
            expr.push_back(this->parseExpression());

            if (this->currentToken()->type == &TokenType::Identifier) {
                AstNode* e = this->parseExpression();
                NodeAssign* valNode = new NodeAssign(new NodeVariable(boost::any_cast<LexerToken>(e->token)), expr[expr.size() - 1]);
                NodeVariable* typeNode = new NodeVariable(new LexerToken("Exception", &TokenType::Identifier));
                // LexerToken* typeNodeToken = this->currentToken();
                // AstNode* typeNode = this->parseFactor();
                NodeDeclare* n = new NodeDeclare(typeNode, boost::any_cast<LexerToken>(e->token), valNode);
                variable.push_back(n);
            }
            else if (this->currentToken()->type == &TokenType::LBrace) {
                variable.push_back(nullptr);
            }
        }

        catchBlock.push_back(this->parseBlockStatement());
        token = this->currentToken();
    }
    if (token->type == &TokenType::Keyword && new Keywords(token->value) == &Keywords::Else) {
        // Eat else
        this->eat(&TokenType::Keyword);

        elseBlock = this->parseBlockStatement();
        
        token = this->currentToken();
    }
    if (token->type == &TokenType::Keyword && new Keywords(token->value) == &Keywords::Finally) {
        // Eat finally
        this->eat(&TokenType::Keyword);

        finallyBlock = this->parseBlockStatement();
        
        token = this->currentToken();
    }
    
    return new NodeTryCatch(block, catchBlock, expr, elseBlock, finallyBlock, tryToken, variable);
}
