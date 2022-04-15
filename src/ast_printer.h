#pragma once

class AstPrinter {
public:
    void printFunc(boost::any string, int indentLevel) {
        std::string str;
        try {
            str = Util::toString(boost::any_cast<AstNode*>(string));
        }
        catch (const boost::bad_any_cast &) {
            str = Util::toString(boost::any_cast<LexerToken*>(string));
        }
        std::cout << (std::string("  ") * indentLevel) << str << std::endl;
    }

    void printTokens(Lexer lexer, int indentLevel) {
        for (auto token : lexer.tokens) {
            this->printFunc(token, indentLevel);
        }
    }

    void printAst(AstNode* node, int indentLevel = 0) {
        if (node == nullptr) {
            return;
        }

        this->printFunc(node, indentLevel);

        if (node->type == &NodeType::Block) {
            for (auto child : ((NodeBlock*) node)->children) {
                this->printAst(child, indentLevel + 1);
            }
        }
        
        else if (node->type == &NodeType::BinOp) {
            // Branch left & right
            this->printAst(((NodeBinOp*) node)->left, indentLevel);
            this->printAst(boost::any_cast<AstNode*>(((NodeBinOp*) node)->right), indentLevel);
        }

        else if (node->type == &NodeType::Assign) {
            this->printAst(((NodeAssign*) node)->lhs, indentLevel);
            this->printAst(boost::any_cast<AstNode*>(((NodeAssign*) node)->value), indentLevel);
        }
        
        else if (node->type == &NodeType::Declare) {
            this->printAst(((NodeDeclare*) node)->value, indentLevel);
        }
        else if (node->type == &NodeType::ArgumentList) {
            this->printFunc("(", indentLevel);

            for (auto argument : ((NodeArgumentList*) node)->arguments) {
                this->printAst(argument, indentLevel + 1);
                this->printFunc(", ", indentLevel + 1);
            }

            this->printFunc(")", indentLevel);
        }
        else if (node->type == &NodeType::FunctionExpression) {
            this->printFunc("<Function>", indentLevel);
            this->printAst(((NodeFunctionExpression*) node)->argumentList, indentLevel);
            this->printAst(((NodeFunctionExpression*) node)->block, indentLevel);
        }
    }
};
