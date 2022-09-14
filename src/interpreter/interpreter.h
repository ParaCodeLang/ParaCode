#pragma once

#include "util.h"
#include "scope.h"
#include "stack.h"
#include "parse/source_location.h"
#include "error.h"
#include "lexer.h"
#include "basic_object.h"
#include "interpreter/env/globals.h"

#include <stdexcept>

class ReturnJump : public std::runtime_error {
public:
    virtual const char* what() const noexcept {
        return "ReturnJump";
    }
};

class Interpreter {
public:
    SourceLocation sourceLocation;
    ErrorList errorList;
    Stack stack;
    
    bool inTry;
    
    Scope* globalScope;
    Scope* m_TopLevelScope;

    Globals m_Globals;

    typedef boost::any (*VisitMethod)(AstNode*);
    std::map<std::string, VisitMethod> visitMethods;

    Interpreter() = default;
    Interpreter(SourceLocation sourceLocation) {
        this->visitMethods = {
            { "visitUnaryOp",         visitUnaryOp },
            { "visitBinOp",           visitBinOp },
            { "visitType",            visitType },
            { "visitDeclare",         visitDeclare },
            { "visitImport",          visitImport },
            { "visitFunctionReturn",  visitFunctionReturn },
            { "visitNumber",          visitNumber },
            { "visitString",          visitString },
        };

        this->sourceLocation = sourceLocation;
        this->errorList = ErrorList();
        // Declare scopes + global scope
        this->stack = Stack();

        this->inTry = false;

        this->globalScope = new Scope(nullptr);
        this->m_TopLevelScope = nullptr;

        // m_Globals is only used for pyimport
        this->m_Globals = Globals();
        this->m_Globals.applyToScope(this->globalScope);
    }

    Scope* currentScope() {
        if (this->m_TopLevelScope != nullptr) {
            return this->m_TopLevelScope;
        }

        return this->globalScope;
    }
    
    void openScope() {
        this->m_TopLevelScope = new Scope(this->currentScope());
    }

    Scope* closeScope() {
        if (this->currentScope() == this->globalScope) {
            throw std::runtime_error("cannot close global scope!");
        }
        this->m_TopLevelScope = this->currentScope()->parent;

        return this->currentScope();
    }

    void error(AstNode* node, ErrorType type, std::string message, bool cont = false, std::string name = "", std::vector<std::string> classnames = {}, BasicObject* object = nullptr) {
        if (name == "" && classnames.empty()) {
            if (type == ErrorType::Syntax) {
                name = "Syntax Error";
                classnames = {"Exception", "SyntaxError"};
            }
            else if (type == ErrorType::DoesNotExist) {
                name = "DoesNotExist Error";
                classnames = {"Exception", "DoesNotExistError"};
            }
            else if (type == ErrorType::TypeError) {
                name = "Type Error";
                classnames = {"Exception", "TypeError"};
            }
            else if (type == ErrorType::MultipleDefinition) {
                name = "Multiple Definition Error";
                classnames = {"Exception", "MultipleDefinitionError"};
            }
            else if (type == ErrorType::ArgumentError) {
                name = "Argument Error";
                classnames = {"Exception", "Argument Error"};
            }
            else if (type == ErrorType::InterruptedError) {
                name = "Interrupted Error";
                classnames = {"Exception", "InterruptedError"};
            }
            else if (type == ErrorType::MacroExpansionError) {
                name = "Macro Expansion Error";
                classnames = {"Exception", "MacroExpansionError"};
            }
            else {
                name = "Exception";
                classnames = {"Exception"};
            }
        }

        std::tuple<int, int> location;

        if (node != nullptr) {
            location = node->location;
        }

        if (!cont && this->inTry) {
            throw InterpreterError("cannot close global scope!");
        }

        Error err = Error(type, location, message, this->sourceLocation.filename, name);
        this->errorList.pushError(err);
        this->errorList.printErrors();

        if (cont || !this->inTry) {
            throw InterpreterError("Interpreter error", node, type, message, cont, name, classnames, object);
        }
    }

    BasicValue* visit(boost::any node, bool allowCasting = false) {
        if (Util::isType<BasicValue>(node)) {
            return boost::any_cast<BasicValue*>(node);
        }

        std::string callerName = Util::format("visit%s", Util::toString(node->type.name));
        if (callerName == "visitBlock") {
            return this->visitBlock(node);
        }
        else if (callerName == "visitAssign") {
            return this->visitAssign(node, allowCasting);
        }
        else if (!this->visitMethods.count(callerName)) {
            throw std::runtime_error("No visitor function defined for node %s", Util::toString(node).c_str());
        }
        
        return this->visitMethods[callerName](node);
    }

    boost::any visitUnaryOp(AstNode* node) {
        std::string funstr = "__noop__";
        
        if (node->token.type == &TokenType::Plus) {
            boost::any val = this->visit(node->expression);
            return new BasicValue(val->value);
        }
        else if (node->token->type == &TokenType::Minus) {
            boost::any val = this->visit(node->expression)
            return new BasicValue(-val->value);
        }
            
        else if (node->token->type == &TokenType::Not) {
            funstr = "__not__";
            // if (val == nullptr || val->value == 0) {
            //     return new BasicValue(1);
            // }
            // else {
            //     return new BasicValue(0);
            // }
        }

        else if (node->token->type == &TokenType::BitwiseNot) {
            funstr = "__bitnot__";
        }

        NodeCall* memberAccessCallNode = new NodeCall(
            new NodeMemberExpression(
                node->expression,
                new LexerToken(funstr, &TokenType::Identifier),
                node->token
            ),
            new NodeArgumentList(
                {},
                node->token
            )
        );

        return this->visit(memberAccessCallNode);
    }

    boost::any visitBinOp(AstNode* node) {
        std::string funstr = "__noop__";
        
        if (node->token->type == &TokenType::Plus) {
            funstr = "__add__";
        }
        else if (node->token->type == &TokenType::Minus) {
            funstr = "__sub__";
        }
        else if (node->token->type == &TokenType::Multiply) {
            funstr = "__mul__";
        }
        else if (node->token->type == &TokenType::Exponentiation) {
            funstr = "__expon__";
        }
        else if (node->token->type == &TokenType::Divide) {
            funstr = "__div__";
        }
        else if (node->token->type == &TokenType::Modulus) {
            funstr = "__mod__";
        }
        else if (node->token->type == &TokenType::LessThan) {
            funstr = "__lt__";
        }
        else if (node->token->type == &TokenType::LessThanEqual) {
            funstr = "__lte__";
        }
        else if (node->token->type == &TokenType::GreaterThan) {
            funstr = "__gt__";
        }
        else if (node->token->type == &TokenType::GreaterThanEqual)) {
            funstr = "__gte__";
        }
        else if (node->token->type == &TokenType::Compare) {
            funstr = "__eql__";
        }
        else if (node->token->type == &TokenType::NotCompare) {
            funstr = "__noteql__";
        }
        else if (node->token->type == &TokenType::And) {
            funstr = "__and__";
        }
        else if (node->token->type == &TokenType::Or) {
            funstr = "__or__";
        }
        else if (node->token->type == &TokenType::BitwiseOr) {
            funstr = "__bitor__";
        }
        else if (node->token->type == &TokenType::BitwiseAnd) {
            funstr = "__bitand__";
        }
        else if (node->token->type == &TokenType::BitwiseXor) {
            funstr = "__bitxor__";
        }
        else if (node->token->type == &TokenType::BitwiseLShift) {
            funstr = "__bitshiftleft__";
        }
        else if (node->token->type == &TokenType::BitwiseRShift) {
            funstr = "__bitshiftright__";
        }
        else if (node->token->type == &TokenType::Spaceship) {
            funstr = "__compare__";
        }
            
        NodeCall* memberAccessCallNode = new NodeCall(
            new NodeMemberExpression(
                node->left,
                new LexerToken(funstr, &TokenType::Identifier),
                node->token
            ),
            new NodeArgumentList(
                {node->right},
                node->token
            )
        );
        return this->visit(memberAccessCallNode);
    }
        
    boost::any visitType(AstNode* node) {
        return boost::any();
    }

    boost::any visitDeclare(AstNode* node) {
        BasicType* typeNodeValue;

        if (Util::isType<NodeSplatArgument>(node)) {
            node = new NodeDeclare(nullptr, node->token, new NodeNone(node->token));
        }
        if (!node->typeNode->empty()) {
            typeNodeValue = boost::any_cast<BasicType*>(this->visit(node->typeNode));
        }

        if (this->currentScope()->findVariableInfo(node->name->value, limit=True) != None) {
            this->error(node, ErrorType::MultipleDefinition, Util::format("multiple definition of '%s'", node->name->value.c_str()));
        }
   
        this->currentScope()->declareVariable(node->name->value, typeNodeValue, node->allowCasting);
        return this->visit(node->value, node->allowCasting);
    }

    boost::any visitImport(AstNode* node) {
        // The imported file is already lexed and parsed from the parser, so this
        // acts like a block and visits the statements inside. This means that if we
        // import inside a function, any variables should only be available to that
        // scope.
        SourceLocation oldSourceLocation = this->sourceLocation;
        this->sourceLocation = node->sourceLocation;

        for (auto child : node->children) {
            this->visit(child);
        }

        this->sourceLocation = oldSourceLocation;
    }

    boost::any visitFunctionReturn(AstNode* node) {
        BasicValue* value = boost::any_cast<BasicValue*>(this->visit(node->valueNode));
        this->stack.push(value);
        throw ReturnJump();
        return boost::any();
    }

    boost::any visitNumber(AstNode* node) {
        return new BasicValue(node->value);
    }

    boost::any visitString(AstNode* node) {
        return new BasicValue(node->value);
    }

    boost::any visitBlock(AstNode* node, bool createScope = true) {
        if (createScope) {
            this->openScope();
        }
        
        // Visit each statement in block
        for (auto child : node->children) {
            this->visit(child);
        }
            
        if (createScope) {
            this->closeScope();
        }
        return boost::any();
    }

    std::tuple<bool, BasicValue*> assignmentTypecheck(AstNode* node, BasicType* typeObject, BasicValue* assignmentValue, bool detailedReturn = false, bool allowCasting = false) {
        if (typeObject == nullptr) {
            this->error(node, ErrorType::TypeError, "Set with decltype but decltype resolved to nullptr");
            if (detailedReturn) {
                return std::make_tuple(false, assignmentValue);
            }
            return std::make_tuple(false, nullptr);
        }
        else if (!Util::isType<BasicType>(typeObject)) {
            this->error(node, ErrorType::TypeError, Util::format("%s is not a valid type object and cannot be used as a declaration type", Util::toString(typeObject).c_str()));
            if (detailedReturn) {
                return std::make_tuple(false, assignmentValue);
            }
            return std::make_tuple(false, nullptr);
        }
        else {
            assignmentType = new BasicValue(assignmentValue)->lookupType(this->globalScope);

            if (Util::isType<BasicObject>(assignmentType)) {
                assignmentType = assignmentValue->parent;
            }

            if (assignmentType == nullptr) {
                this->error(node, ErrorType::TypeError, Util::format("Assignment requires type %s but could not resolve a runtime type of assignment value", Util::toString(typeObject).c_str()));
                if (detailedReturn) {
                    return std::make_tuple(false, assignmentValue);
                }
                return std::make_tuple(false, nullptr);
            }
            if (Util::toString<BasicValue>(assignmentType)) {
                assignmentType = assignmentType->extractValue();
            }

            if (!Util::isType<BasicType>(assignmentType)) {
                this->error(node, ErrorType::TypeError, Util::format("%s is not a valid runtime type object", Util::toString(assignmentType).c_str()));
                if (detailedReturn) {
                    return std::make_tuple(false, assignmentValue);
                }
                return std::make_tuple(false, nullptr);
            }
    
            if (!typeObject->compareType(assignmentType)) {
                if (allowCasting) {
                    try {
                        assignmentValue = builtinObjectNew(BuiltinFunctionArguments(this, typeObject, {assignmentValue}, node));
                        assignmentType = typeObject;
                    }
                    catch (const InterpreterError &) {
                        this->error(node, ErrorType::TypeError, Util::format("Attempted to assign <%s> to a value of type <%s>", typeObject->friendlyTypename.c_str(), assignmentType->friendlyTypename.c_str()));
                        if (detailedReturn) {
                            return std::make_tuple(false, assignmentValue);
                        }
                        return std::make_tuple(false, nullptr);
                    }
                }
                else {
                    this->error(node, ErrorType::TypeError, Util::format("Attempted to assign <%s> to a value of type <%s>", typeObject->friendlyTypename.c_str(), assignmentType->friendlyTypename.c_str()));
                    if (detailedReturn) {
                        return std::make_tuple(false, assignmentValue);
                    }
                    return std::make_tuple(false, nullptr);
                }
            }
        }

        if (detailedReturn) {
            return std::make_tuple(true, assignmentValue);
        }
        return std::make_tuple(true, nullptr);
    }

    SymbolInfo* walkVariable(NodeVariable* node) {
        SymbolInfo* var = this->currentScope.findVariableInfo(node->value);
        if (var == nullptr) {
            this->error(node, ErrorType::DoesNotExist, Util::format("Referencing undefined variable '%s'", node->value.c_str()));
            return nullptr;
        }

        return var;
    }

    def basicValueToObject(node, target) {
        target = (new BasicValue(target))->extractBasicValue();

        if (!Util::isType<BasicObject>(target)) {
            target_type_object = target.lookup_type(this->global_scope).extractBasicValue()

            if target_type_object is None {
                this->error(node, ErrorType::TypeError, "invalid member access: target {} is not a BasicObject".format(target))
                return None;
            }

            // for a string this would basically mean:
            // "hello ".append("world")
            // -> Str.new("hello ").append("world")
            target = builtinObjectNew(BuiltinFunctionArguments(interpreter=self, this_object=target_type_object, arguments=[target], node=node));
        }

        return target;
    }

    std::tuple<BasicObject*, ObjectMember> walkMemberExpression(AstNode* node) {
        target = this->visit(node.lhs);

        target = this->basicValueToObject(node, target)

        member = target.lookupMember(node->identifier-value)

        if (member == nullptr) {
            this->error(node, ErrorType.TypeError, "{} has no direct or inherited member `{}`".format(objToString(this, node, target), node->identifier->value))
        }

        return (target, member)

    boost::any visitAssign(AstNode* node, bool allowCasting = false) {
        if (Util::isType<NodeVariable>(node->lhs)) {
            node->allowCasting = allowCasting;
            SymbolInfo* targetInfo = this->walkVariable(node->lhs);
            BasicValue* targetValue = targetInfo->valueWrapper;

            value = this->visit(node->value);
            // TYPE CHECK
            if (targetInfo->declltype != nullptr) {
                std::tuple<bool, BasicValue*> typecheck = this->assignmentTypecheck(node->lhs, targetInfo->declltype, value, true, allowCasting);
                bool typecheckValue = std::get<0>(typecheck);
                BasicValue* value = std::get<1>(typecheck);

                if (!typecheckValue) {
                    return boost::any();
                }
            }

            targetValue->assignValue(value);
            return value;
        }
        else if (isinstance(node->lhs, NodeMemberExpression)) {
            std::tuple<bool, BasicValue*> typecheck = this->assignmentTypecheck(node->lhs, targetInfo->declltype, value, true, allowCasting);
            bool typecheckValue = std::get<0>(typecheck);
            BasicValue* value = std::get<1>(typecheck);
            (target, member) = this->walk_member_expression(node->lhs);

            if not isinstance(target, BasicObject):
                this->error(node, ErrorType.TypeError, "member expression not assignable");
                return boost::any();

            target_type = target.parent;

            value = this->visit(node->value);
            target.assignMember(member.name, value);
            return value;
        }
        elif isinstance(node->lhs, NodeArrayAccessExpression):
            member_access_call_node = NodeCall(
                NodeMemberExpression(
                    node->lhs.lhs,
                    LexerToken("__set__", &TokenType::Identifier),
                    node->lhs.token
                ),
                NodeArgumentList(
                    [node->lhs.access_expr, node->value],

                    node->lhs.token
                )
            )

            return this->visit(member_access_call_node)

        else {
            this->error(node, ErrorType::TypeError, "cannot assign {}".format(node->lhs))

            return boost::any();
        }
    }
};
