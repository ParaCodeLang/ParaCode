#pragma once

#include "lexer.h"

#include <boost/any.hpp>

class NodeType {
public:
    static std::map<std::string, NodeType> s_Values;

    static NodeType Empty;
    static NodeType BinOp;
    static NodeType Number;
    static NodeType String;
    static NodeType UnaryOp;
    static NodeType Block;
    static NodeType Assign;
    static NodeType Variable;
    static NodeType Type;
    static NodeType Declare;
    static NodeType Call;
    static NodeType Import;
    static NodeType While;
    static NodeType For;
    static NodeType IfStatement;
    static NodeType Try;
    static NodeType ArgumentList;
    static NodeType SplatArgument;
    static NodeType FunctionReturn;
    static NodeType FunctionExpression;
    static NodeType Macro;
    static NodeType Mixin;
    static NodeType ArrayExpression;
    static NodeType ObjectExpression;
    static NodeType MemberExpression;
    static NodeType ArrayAccessExpression;

    std::string name;
    boost::any value;

    NodeType() = default;
    NodeType(std::string name, boost::any value) {
        this->name = name;
        this->value = value;
    }

    inline bool operator==(const NodeType& rhs) { return this->name == rhs.name; }
    inline bool operator!=(const NodeType& rhs) { return !(*this == rhs); }
};

class AstNode {
public:
    std::tuple<int, int> location = std::make_tuple(0, 0);
    NodeType* type;
    boost::any* token;
    
    AstNode() = default;
    AstNode(NodeType* type, boost::any* token) {
        this->type = type;
        this->token = token;
        try {
            this->location = boost::any_cast<LexerToken>(token)->location;
        }
        catch (const boost::bad_any_cast &) {
            this->location = boost::any_cast<AstNode>(token)->location;
        }
    }
    AstNode(NodeType* type, boost::any token) {
        this->type = type;
        this->token = &token;
        try {
            this->location = boost::any_cast<LexerToken>(token).location;
        }
        catch (const boost::bad_any_cast &) {
            this->location = boost::any_cast<AstNode>(token).location;
        }
    }

    AstNode thisObject() {
        return *this;
    }

    std::string toString() {
        try {
            return Util::format("AstNode[{%s}, {%s}]", this->type->name.c_str(), boost::any_cast<LexerToken*>(this->token));
        }
        catch (const boost::bad_any_cast &) {
            return Util::format("AstNode[{%s}]", this->type->name.c_str());
        }
    }

    virtual bool hasValue() { return false; }
};

class NodeNone : public AstNode {
public:
    NodeNone(LexerToken* token) : AstNode(&NodeType::Empty, token) {}
};

// Binary op node; LEFT [+-*/] RIGHT
class NodeBinOp : public AstNode {
public:
    AstNode* left;
    LexerToken* token;
    boost::any right;

    NodeBinOp(AstNode* left, LexerToken* token, boost::any right) : AstNode(&NodeType::BinOp, token) {
        this->left = left;
        this->token = token;
        this->right = right;
    }
};

class NodeNumber : public AstNode {
public:
    LexerToken* token;
    boost::any value;

    NodeNumber(LexerToken* token) : AstNode(&NodeType::Number, token) {
        this->token = token;
        // std::stoi(..., 0) for guessing hexadecimal etc.
        if (boost::any_cast<std::string>(token->value).find('.') != std::string::npos) {
            this->value = std::stof(boost::any_cast<std::string>(token->value));
        }
        else {
            this->value = std::stoi(boost::any_cast<std::string>(token->value), nullptr, 0);
        }
    }

    virtual bool hasValue() { return true; }
};

class NodeString : public AstNode {
public:
    std::string value;

    NodeString(LexerToken* token) : AstNode(&NodeType::String, token) {
        this->value = Util::toString(token->value).substr(1, -1);
    }

    virtual bool hasValue() { return true; }
};

// Unary node; switches signage for values, '!' operator
class NodeUnaryOp : public AstNode {
public:
    LexerToken* token;
    AstNode* expression;

    NodeUnaryOp(LexerToken* token, AstNode* expression) : AstNode(&NodeType::UnaryOp, token) {
        this->token = token;
        this->expression = expression;
    }
};

// Block node; parent to multiple nodes
class NodeBlock : public AstNode {
public:
    std::vector<AstNode*> children;

    NodeBlock(LexerToken* token) : AstNode(&NodeType::Block, token) {
        this->children = {};
    }
};

// Type node; Holds type info for variable
class NodeVarType : public AstNode {
public:
    LexerToken* token;

    NodeVarType(LexerToken* token) : AstNode(&NodeType::Type, token) {
        this->token = token;
    }

    bool isTypeType() {
        return this->token->value == "type";
    }
};

// Declare node; declare variable or function
class NodeDeclare : public AstNode {
public:
    AstNode* typeNode;
    LexerToken* name;
    AstNode* value;
    bool allowCasting;
    
    NodeDeclare(AstNode* type, LexerToken* name, AstNode* value, bool allowCasting = false) : AstNode(&NodeType::Declare, name) {
        this->typeNode = type;
        this->name = name;
        this->value = value;
        this->allowCasting = allowCasting;
    }

    virtual bool hasValue() { return true; }
};

class NodeImport : public AstNode {
public:
    std::vector<AstNode*> children;
    SourceLocation sourceLocation;
    
    NodeImport(LexerToken* filename, SourceLocation sourceLocation) : AstNode(&NodeType::Import, filename) {
        this->children = {};
        this->sourceLocation = sourceLocation;
    }
    NodeImport(LexerToken* filename, SourceLocation* sourceLocation) : AstNode(&NodeType::Import, filename) {
        this->children = {};
        this->sourceLocation = *sourceLocation;
    }
};

class NodeWhile : public AstNode {
public:
    NodeBlock* block;
    AstNode* expr;
    
    NodeWhile(AstNode* expr, NodeBlock* block, LexerToken* token) : AstNode(&NodeType::While, token) {
        this->block = block;
        this->expr = expr;
    }
};

class NodeFor : public AstNode {
public:
    LexerToken* varToken;
    NodeBlock* block;
    AstNode* expr;
    
    NodeFor(LexerToken* varToken, AstNode* expr, NodeBlock* block, LexerToken* token) : AstNode(&NodeType::For, token) {
        this->varToken = varToken;
        this->block = block;
        this->expr = expr;
    }
};

class NodeArgumentList : public AstNode {
public:
    std::deque<AstNode*> arguments;

    NodeArgumentList(std::deque<AstNode*> arguments, LexerToken* token) : AstNode(&NodeType::ArgumentList, token) {
        this->arguments = arguments;
    }
};

class NodeCall : public AstNode {
public:
    AstNode* lhs;
    NodeArgumentList* argumentList;
    
    NodeCall(AstNode* lhs, NodeArgumentList* argumentList) : AstNode(&NodeType::Call, boost::any_cast<LexerToken*>(lhs->token)) {
        this->lhs = lhs;
        this->argumentList = argumentList;
    }
};

// Assignment node; Var = Value
class NodeAssign : public AstNode {
public:
    AstNode* lhs;
    boost::any value;
    
    NodeAssign(AstNode* lhs, boost::any value) : AstNode(&NodeType::Assign, value) {
        this->lhs = lhs;
        this->value = value;
    }

    virtual bool hasValue() { return true; }
};

// Variable node; request value of variable
class NodeVariable : public AstNode {
public:
    LexerToken* token;
    std::string value;
    bool allowCasting;
    
    NodeVariable(LexerToken* token, bool allowCasting = false) : AstNode(&NodeType::Variable, token) {
        this->token = token;
        this->value = token->value;
        this->allowCasting = allowCasting;
    }

    virtual bool hasValue() { return true; }
};

class NodeIfStatement : public AstNode {
public:
    AstNode* expr;
    NodeBlock* block;
    AstNode* elseBlock;
    
    NodeIfStatement(AstNode* expr, NodeBlock* block, AstNode* elseBlock, LexerToken* token) : AstNode(&NodeType::IfStatement, token) {
        this->expr = expr;
        this->block = block;
        this->elseBlock = elseBlock;
    }
};

class NodeTryCatch : public AstNode {
public:
    NodeBlock* block;
    std::vector<NodeBlock*> catchBlock;
    std::vector<boost::any> expr;
    NodeBlock* elseBlock;
    NodeBlock* finallyBlock;
    std::vector<NodeDeclare*> variable;
    
    NodeTryCatch(NodeBlock* block, std::vector<NodeBlock*> catchBlock, std::vector<boost::any> expr, NodeBlock* elseBlock, NodeBlock* finallyBlock, LexerToken* token, std::vector<NodeDeclare*> variable) : AstNode(&NodeType::Try, token) {
        this->block = block;
        this->catchBlock = catchBlock;
        this->expr = expr;
        this->elseBlock = elseBlock;
        this->finallyBlock = finallyBlock;
        this->variable = variable;
    }
};

class NodeSplatArgument : public AstNode {
public:
    AstNode* expr;
    
    NodeSplatArgument(AstNode* expr, LexerToken* token) : AstNode(&NodeType::SplatArgument, token) {
        this->expr = expr;
    }
};

class NodeFunctionExpression : public AstNode {
public:
    NodeArgumentList* argumentList;
    NodeBlock* block;
    
    NodeFunctionExpression(NodeArgumentList* argumentList, NodeBlock* block) : AstNode(&NodeType::FunctionExpression, block) {
        this->argumentList = argumentList;
        this->block = block;
    }
};

class NodeFunctionReturn : public AstNode {
public:
    AstNode* valueNode;
    
    NodeFunctionReturn(AstNode* valueNode, LexerToken* token) : AstNode(&NodeType::FunctionReturn, token) {
        this->valueNode = valueNode;
    }
};

class NodeMacro : public AstNode {
public:
    AstNode* expr;
    
    NodeMacro(AstNode* expr, LexerToken* token) : AstNode(&NodeType::Macro, token) {
        this->expr = expr;
    }
};

class NodeMixin : public AstNode {
public:
    std::vector<LexerToken*> tokens;
    
    NodeMixin(std::vector<LexerToken*> tokens, LexerToken* token) : AstNode(&NodeType::Mixin, token) {
        this->tokens = tokens;
    }
};

class NodeArrayExpression : public AstNode {
public:
    std::vector<AstNode*> members;
    bool isDictionary;
    
    NodeArrayExpression(std::vector<AstNode*> members, LexerToken* token, bool isDictionary = false) : AstNode(&NodeType::ArrayExpression, token) {
        // Members are var decls
        this->members = members;
        this->isDictionary = isDictionary;
    }
};

class NodeObjectExpression : public AstNode {
public:
    NodeType* type;
    std::vector<NodeDeclare*> members;
    
    NodeObjectExpression(std::vector<NodeDeclare*> members) {
        // Members are var decls
        this->type = &NodeType::ObjectExpression;
        this->members = members;
    }
};

class NodeMemberExpression : public AstNode {
public:
    NodeType* type;
    AstNode* lhs;
    LexerToken* identifier;
    LexerToken* token;
    
    NodeMemberExpression(AstNode* lhs, LexerToken* identifier, LexerToken* token) {
        // Members are var decls
        this->type = &NodeType::MemberExpression;
        this->lhs = lhs;
        this->identifier = identifier;
        this->token = token;
    }
};

class NodeArrayAccessExpression : public AstNode {
public:
    NodeType* type;
    AstNode* lhs;
    AstNode* accessExpr;
    LexerToken* token;
    
    NodeArrayAccessExpression(AstNode* lhs, AstNode* accessExpr, LexerToken* token) {
        // Members are var decls
        this->type = &NodeType::ArrayAccessExpression;
        this->lhs = lhs;
        this->accessExpr = accessExpr;
        this->token = token;
    }
};
