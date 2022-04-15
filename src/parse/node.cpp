#include "node.h"

NodeType NodeType::Empty = NodeType("Empty", 1);
NodeType NodeType::BinOp = NodeType("BinOp", 2);
NodeType NodeType::Number = NodeType("Number", 3);
NodeType NodeType::String = NodeType("String", 4);
NodeType NodeType::UnaryOp = NodeType("UnaryOp", 5);
NodeType NodeType::Block = NodeType("Block", 6);
NodeType NodeType::Assign = NodeType("Assign", 7);
NodeType NodeType::Variable = NodeType("Variable", 8);
NodeType NodeType::Type = NodeType("Type", 9);
NodeType NodeType::Declare = NodeType("Declare", 10);
NodeType NodeType::Call = NodeType("Call", 11);
NodeType NodeType::Import = NodeType("Import", 12);
NodeType NodeType::While = NodeType("While", 13);
NodeType NodeType::For = NodeType("For", 14);
NodeType NodeType::IfStatement = NodeType("IfStatement", 15);
NodeType NodeType::Try = NodeType("Try", 16);
NodeType NodeType::ArgumentList = NodeType("ArgumentList", 17);
NodeType NodeType::SplatArgument = NodeType("SplatArgument", 18);
NodeType NodeType::FunctionReturn = NodeType("FunctionReturn", 19);
NodeType NodeType::FunctionExpression = NodeType("FunctionExpression", 20);
NodeType NodeType::Macro = NodeType("Macro", 21);
NodeType NodeType::Mixin = NodeType("Mixin", 22);
NodeType NodeType::ArrayExpression = NodeType("ArrayExpression", 23);
NodeType NodeType::ObjectExpression = NodeType("ObjectExpression", 24);
NodeType NodeType::MemberExpression = NodeType("MemberExpression", 25);
NodeType NodeType::ArrayAccessExpression = NodeType("ArrayAccessExpression", 26);

std::map<std::string, NodeType> NodeType::s_Values = {
    { NodeType::Empty.name, NodeType::Empty },
    { NodeType::BinOp.name, NodeType::BinOp },
    { NodeType::Number.name, NodeType::Number },
    { NodeType::String.name, NodeType::String },
    { NodeType::UnaryOp.name, NodeType::UnaryOp },
    { NodeType::Block.name, NodeType::Block },
    { NodeType::Assign.name, NodeType::Assign },
    { NodeType::Variable.name, NodeType::Variable },
    { NodeType::Type.name, NodeType::Type },
    { NodeType::Declare.name, NodeType::Declare },
    { NodeType::Call.name, NodeType::Call },
    { NodeType::Import.name, NodeType::Import },
    { NodeType::While.name, NodeType::While },
    { NodeType::For.name, NodeType::For },
    { NodeType::IfStatement.name, NodeType::IfStatement },
    { NodeType::Try.name, NodeType::Try },
    { NodeType::ArgumentList.name, NodeType::ArgumentList },
    { NodeType::SplatArgument.name, NodeType::SplatArgument },
    { NodeType::FunctionReturn.name, NodeType::FunctionReturn },
    { NodeType::FunctionExpression.name, NodeType::FunctionExpression },
    { NodeType::Macro.name, NodeType::Macro },
    { NodeType::Mixin.name, NodeType::Mixin },
    { NodeType::ArrayExpression.name, NodeType::ArrayExpression },
    { NodeType::ObjectExpression.name, NodeType::ObjectExpression },
    { NodeType::MemberExpression.name, NodeType::MemberExpression },
    { NodeType::ArrayAccessExpression.name, NodeType::ArrayAccessExpression }
};

namespace Util {
    template<> std::string toString(const AstNode& t) { return t.toString(); }
}
