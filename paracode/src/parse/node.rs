use std::fmt;
use std::convert::AsRef;

use strum_macros::AsRefStr;

use crate::lexer::LexerToken;
use crate::parse::source_location::SourceLocation;

#[derive(PartialEq, Debug, Clone)]
pub enum NumberType {
    Int(i32),
    Float(f32),
}

#[derive(Eq, PartialEq, Debug, EnumString, strum_macros::Display, AsRefStr)]
pub enum NodeType {
    #[strum(serialize="Empty", serialize="1")]
    Empty,
    #[strum(serialize="BinOp", serialize="2")]
    BinOp,
    #[strum(serialize="Number", serialize="3")]
    Number,
    #[strum(serialize="String", serialize="4")]
    String,
    #[strum(serialize="UnaryOp", serialize="5")]
    UnaryOp,
    #[strum(serialize="Block", serialize="6")]
    Block,
    #[strum(serialize="Assign", serialize="7")]
    Assign,
    #[strum(serialize="Variable", serialize="8")]
    Variable,
    #[strum(serialize="Type", serialize="9")]
    Type,
    #[strum(serialize="Declare", serialize="10")]
    Declare,
    #[strum(serialize="Call", serialize="11")]
    Call,
    #[strum(serialize="Import", serialize="12")]
    Import,
    #[strum(serialize="While", serialize="13")]
    While,
    #[strum(serialize="For", serialize="14")]
    For,
    #[strum(serialize="IfStatement", serialize="15")]
    IfStatement,
    #[strum(serialize="Try", serialize="16")]
    Try,
    #[strum(serialize="ArgumentList", serialize="17")]
    ArgumentList,
    #[strum(serialize="SplatArgument", serialize="18")]
    SplatArgument,
    #[strum(serialize="FunctionReturn", serialize="19")]
    FunctionReturn,
    #[strum(serialize="FunctionExpression", serialize="20")]
    FunctionExpression,
    #[strum(serialize="Macro", serialize="21")]
    Macro,
    #[strum(serialize="Mixin", serialize="22")]
    Mixin,
    #[strum(serialize="ArrayExpression", serialize="23")]
    ArrayExpression,
    #[strum(serialize="ObjectExpression", serialize="24")]
    ObjectExpression,
    #[strum(serialize="MemberExpression", serialize="25")]
    MemberExpression,
    #[strum(serialize="ArrayAccessExpression", serialize="26")]
    ArrayAccessExpression
}

#[derive(Clone)]
pub enum NodeTokenType<'a> {
    Token(&'a LexerToken),
    Node(&'a dyn AstNode<'a>),
}
impl<'a> fmt::Display for NodeTokenType<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return match self {
            NodeTokenType::Token(tok) => write!(f, "{}", tok),
            NodeTokenType::Node(node) => write!(f, "{}", node),
        }
    }
}
impl<'a> fmt::Debug for NodeTokenType<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return match self {
            NodeTokenType::Token(tok) => write!(f, "{:?}", tok),
            NodeTokenType::Node(node) => write!(f, "{:?}", node),
        }
    }
}

pub trait AstNode<'a>: fmt::Debug + fmt::Display {
    fn node_type(&self) -> &NodeType;
    fn token(&self) -> &Option<NodeTokenType<'a>>;
    fn location(&self) -> (i32, i32);
}

#[macro_export]
macro_rules! impl_astnode {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl<'a> AstNode<'a> for $name<'a> {
            fn node_type(&self) -> &NodeType {
                return &self.ty;
            }
            
            fn token(&self) -> &Option<NodeTokenType<'a>> {
                return &self.tok;
            }

            fn location(&self) -> (i32, i32) {
                return self.loc;
            }
        }
    };
}
#[macro_export]
macro_rules! impl_astnode__ref_token {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl<'a> AstNode<'a> for $name<'a> {
            fn node_type(&self) -> &NodeType {
                return &self.ty;
            }
            
            fn token(&self) -> &Option<NodeTokenType<'a>> {
                return self.tok;
            }

            fn location(&self) -> (i32, i32) {
                return self.loc;
            }
        }
    };
}
#[macro_export]
macro_rules! impl_astnode_displays {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl<'a> std::fmt::Display for $name<'a> {
            fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
                return match self.token() {
                    Some(tok) => write!(f, "AstNode[{}, {}]", self.node_type().as_ref(), tok),
                    None => write!(f, "AstNode[{}]", self.node_type().as_ref()),
                }
            }
        }
        impl<'a> std::fmt::Debug for $name<'a> {
            fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
                return write!(f, "{}", self);
            }
        }
    };
}

pub struct NodeNone<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),
}
impl<'a> NodeNone<'a> {
    pub fn new(token: &'a LexerToken) -> NodeNone<'a> {
        return NodeNone {
            ty: NodeType::Empty,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location
        }
    }
}
impl_astnode!(NodeNone);
impl_astnode_displays!(NodeNone);

// Binary op node; LEFT [+-*/] RIGHT
pub struct NodeBinOp<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    left: &'a dyn AstNode<'a>,
    right: &'a dyn AstNode<'a>,
}
impl<'a> NodeBinOp<'a> {
    pub fn new(left: &'a dyn AstNode<'a>, token: &'a LexerToken, right: &'a dyn AstNode<'a>) -> NodeBinOp<'a> {
        return NodeBinOp {
            ty: NodeType::BinOp,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            left: left,
            right: right
        }
    }
}
impl_astnode!(NodeBinOp);
impl_astnode_displays!(NodeBinOp);

pub struct NodeNumber<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    value: NumberType,
}
impl<'a> NodeNumber<'a> {
    pub fn new(token: &'a LexerToken) -> NodeNumber<'a> {
        let value: NumberType;
        if token.value.contains(".") {
            value = NumberType::Float(lexical::parse::<f32, _>(&token.value).unwrap());
        }
        else {
            value = NumberType::Int(lexical::parse::<i32, _>(&token.value).unwrap());
        }
        return NodeNumber {
            ty: NodeType::Number,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            value: value
        }
    }
}
impl_astnode!(NodeNumber);
impl_astnode_displays!(NodeNumber);

pub struct NodeString<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    value: String,
}
impl<'a> NodeString<'a> {
    pub fn new(token: &'a LexerToken) -> NodeString<'a> {
        return NodeString {
            ty: NodeType::String,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            value: token.value[1..token.value.len() - 1].to_string()
        }
    }
}
impl_astnode!(NodeString);
impl_astnode_displays!(NodeString);

// Unary node; switches signage for values, '!' operator
pub struct NodeUnaryOp<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    expression: &'a dyn AstNode<'a>,
}
impl<'a> NodeUnaryOp<'a> {
    pub fn new(token: &'a LexerToken, expression: &'a dyn AstNode<'a>) -> NodeUnaryOp<'a> {
        return NodeUnaryOp {
            ty: NodeType::UnaryOp,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            expression: expression
        }
    }
}
impl_astnode!(NodeUnaryOp);
impl_astnode_displays!(NodeUnaryOp);

// Block node; parent to multiple nodes
pub struct NodeBlock<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    children: Vec<&'a dyn AstNode<'a>>,
}
impl<'a> NodeBlock<'a> {
    pub fn new(token: &'a LexerToken) -> NodeBlock<'a> {
        return NodeBlock {
            ty: NodeType::Block,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            children: vec![]
        }
    }
}
impl_astnode!(NodeBlock);
impl_astnode_displays!(NodeBlock);

// Type node; Holds type info for variable
pub struct NodeVarType<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),
}
impl<'a> NodeVarType<'a> {
    pub fn new(token: &'a LexerToken) -> NodeVarType<'a> {
        return NodeVarType {
            ty: NodeType::Type,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location
        }
    }

    pub fn is_type_type(&self) -> bool {
        return match self.tok.as_ref().unwrap() {
            NodeTokenType::Token(tok) => tok.value == "type",
            NodeTokenType::Node(_) => unreachable!(),
        }
    }
}
impl_astnode!(NodeVarType);
impl_astnode_displays!(NodeVarType);

// Declare node; declare variable or function
pub struct NodeDeclare<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    type_node: Option<&'a dyn AstNode<'a>>,
    name: &'a LexerToken,
    value: &'a dyn AstNode<'a>,
    allow_casting: bool,
}
impl<'a> NodeDeclare<'a> {
    pub fn new(ty: Option<&'a dyn AstNode<'a>>, name: &'a LexerToken, value: &'a dyn AstNode<'a>, allow_casting: bool) -> NodeDeclare<'a> {
        return NodeDeclare {
            ty: NodeType::Declare,
            tok: Some(NodeTokenType::Token(name)),
            loc: name.location,

            type_node: ty,
            name: name,
            value: value,
            allow_casting: allow_casting
        }
    }
}
impl_astnode!(NodeDeclare);
impl_astnode_displays!(NodeDeclare);

pub struct NodeImport<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    children: Vec<&'a dyn AstNode<'a>>,
    source_location: SourceLocation,
}
impl<'a> NodeImport<'a> {
    pub fn new(filename: &'a LexerToken, source_location: SourceLocation) -> NodeImport<'a> {
        return NodeImport {
            ty: NodeType::Import,
            tok: Some(NodeTokenType::Token(filename)),
            loc: filename.location,
            
            children: vec![],
            source_location: source_location
        }
    }
}
impl_astnode!(NodeImport);
impl_astnode_displays!(NodeImport);

pub struct NodeWhile<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    block: &'a NodeBlock<'a>,
    expr: &'a dyn AstNode<'a>,
}
impl<'a> NodeWhile<'a> {
    pub fn new(expr: &'a dyn AstNode<'a>, block: &'a NodeBlock<'a>, token: &'a LexerToken) -> NodeWhile<'a> {
        return NodeWhile {
            ty: NodeType::While,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            block: block,
            expr: expr
        }
    }
}
impl_astnode!(NodeWhile);
impl_astnode_displays!(NodeWhile);

pub struct NodeFor<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    var_token: &'a LexerToken,
    block: &'a NodeBlock<'a>,
    expr: &'a dyn AstNode<'a>,
}
impl<'a> NodeFor<'a> {
    pub fn new(var_token: &'a LexerToken, expr: &'a dyn AstNode<'a>, block: &'a NodeBlock<'a>, token: &'a LexerToken) -> NodeFor<'a> {
        return NodeFor {
            ty: NodeType::For,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            var_token: var_token,
            block: block,
            expr: expr
        }
    }
}
impl_astnode!(NodeFor);
impl_astnode_displays!(NodeFor);

pub struct NodeCall<'a> {
    ty: NodeType,
    tok: &'a Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    lhs: &'a dyn AstNode<'a>,
    argument_list: &'a NodeArgumentList<'a>,
}
impl<'a> NodeCall<'a> {
    pub fn new(lhs: &'a dyn AstNode<'a>, argument_list: &'a NodeArgumentList<'a>) -> NodeCall<'a> {
        return NodeCall {
            ty: NodeType::Call,
            tok: lhs.token(),
            loc: match lhs.token() {
                Some(t) => match t {
                    NodeTokenType::Token(tok) => tok.location,
                    NodeTokenType::Node(node) => node.location(),
                },
                None => (0, 0),
            },

            lhs: lhs,
            argument_list: argument_list
        }
    }
}
impl_astnode__ref_token!(NodeCall);
impl_astnode_displays!(NodeCall);

// Assignment node; Var = Value
pub struct NodeAssign<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    lhs: &'a dyn AstNode<'a>,
    value: &'a dyn AstNode<'a>,
}
impl<'a> NodeAssign<'a> {
    pub fn new(lhs: &'a dyn AstNode<'a>, value: &'a dyn AstNode<'a>) -> NodeAssign<'a> {
        return NodeAssign {
            ty: NodeType::Assign,
            tok: Some(NodeTokenType::Node(value)),
            loc: value.location(),

            lhs: lhs,
            value: value
        }
    }
}
impl_astnode!(NodeAssign);
impl_astnode_displays!(NodeAssign);

// Variable node; request value of variable
pub struct NodeVariable<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    value: &'a String,
    allow_casting: bool,
}
impl<'a> NodeVariable<'a> {
    pub fn new(token: &'a LexerToken, allow_casting: bool) -> NodeVariable<'a> {
        return NodeVariable {
            ty: NodeType::Variable,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            value: &token.value,
            allow_casting: allow_casting
        }
    }
}
impl_astnode!(NodeVariable);
impl_astnode_displays!(NodeVariable);

pub struct NodeIfStatement<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    expr: &'a dyn AstNode<'a>,
    block: &'a NodeBlock<'a>,
    else_block: Option<&'a dyn AstNode<'a>>,
}
impl<'a> NodeIfStatement<'a> {
    pub fn new(expr: &'a dyn AstNode<'a>, block: &'a NodeBlock<'a>, else_block: Option<&'a dyn AstNode<'a>>, token: &'a LexerToken) -> NodeIfStatement<'a> {
        return NodeIfStatement {
            ty: NodeType::IfStatement,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            expr: expr,
            block: block,
            else_block: else_block
        }
    }
}
impl_astnode!(NodeIfStatement);
impl_astnode_displays!(NodeIfStatement);

pub struct NodeTryCatch<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    block: &'a NodeBlock<'a>,
    catch_block: Vec<&'a NodeBlock<'a>>,
    expr: Vec<&'a dyn AstNode<'a>>,
    else_block: Option<&'a dyn AstNode<'a>>,
    finally_block: Option<&'a dyn AstNode<'a>>,
    variable: Option<&'a NodeDeclare<'a>>,
}
impl<'a> NodeTryCatch<'a> {
    pub fn new(block: &'a NodeBlock<'a>, catch_block: Vec<&'a NodeBlock<'a>>, expr: Vec<&'a dyn AstNode<'a>>, else_block: Option<&'a dyn AstNode<'a>>, finally_block: Option<&'a dyn AstNode<'a>>, token: &'a LexerToken, variable: Option<&'a NodeDeclare<'a>>) -> NodeTryCatch<'a> {
        return NodeTryCatch {
            ty: NodeType::Try,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            block: block,
            catch_block: catch_block,
            expr: expr,
            else_block: else_block,
            finally_block: finally_block,
            variable: variable
        }
    }
}
impl_astnode!(NodeTryCatch);
impl_astnode_displays!(NodeTryCatch);

pub struct NodeArgumentList<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    arguments: Vec<NodeTokenType<'a>>,
}
impl<'a> NodeArgumentList<'a> {
    pub fn new(token: &'a LexerToken) -> NodeArgumentList<'a> {
        return NodeArgumentList {
            ty: NodeType::ArgumentList,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            arguments: vec![]
        }
    }
}
impl_astnode!(NodeArgumentList);
impl_astnode_displays!(NodeArgumentList);

pub struct NodeSplatArgument<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    expr: &'a dyn AstNode<'a>,
}
impl<'a> NodeSplatArgument<'a> {
    pub fn new(expr: &'a dyn AstNode<'a>, token: &'a LexerToken) -> NodeSplatArgument<'a> {
        return NodeSplatArgument {
            ty: NodeType::SplatArgument,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            expr: expr
        }
    }
}
impl_astnode!(NodeSplatArgument);
impl_astnode_displays!(NodeSplatArgument);

pub struct NodeFunctionExpression<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    block: &'a NodeBlock<'a>,
    argument_list: &'a NodeArgumentList<'a>,
}
impl<'a> NodeFunctionExpression<'a> {
    pub fn new(argument_list: &'a NodeArgumentList<'a>, block: &'a NodeBlock<'a>) -> NodeFunctionExpression<'a> {
        return NodeFunctionExpression {
            ty: NodeType::FunctionExpression,
            tok: Some(NodeTokenType::Node(block)),
            loc: block.location(),

            block: block,
            argument_list: argument_list
        }
    }
}
impl_astnode!(NodeFunctionExpression);
impl_astnode_displays!(NodeFunctionExpression);

pub struct NodeFunctionReturn<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    value_node: &'a dyn AstNode<'a>,
}
impl<'a> NodeFunctionReturn<'a> {
    pub fn new(value_node: &'a dyn AstNode<'a>, token: &'a LexerToken) -> NodeFunctionReturn<'a> {
        return NodeFunctionReturn {
            ty: NodeType::FunctionReturn,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            value_node: value_node
        }
    }
}
impl_astnode!(NodeFunctionReturn);
impl_astnode_displays!(NodeFunctionReturn);

pub struct NodeMacro<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    expr: &'a NodeCall<'a>,
}
impl<'a> NodeMacro<'a> {
    pub fn new(expr: &'a NodeCall<'a>, token: &'a LexerToken) -> NodeMacro<'a> {
        return NodeMacro {
            ty: NodeType::Macro,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            expr: expr
        }
    }
}
impl_astnode!(NodeMacro);
impl_astnode_displays!(NodeMacro);

pub struct NodeMixin<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    tokens: Vec<&'a LexerToken>,
}
impl<'a> NodeMixin<'a> {
    pub fn new(tokens: Vec<&'a LexerToken>, token: &'a LexerToken) -> NodeMixin<'a> {
        return NodeMixin {
            ty: NodeType::Mixin,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            tokens: tokens
        }
    }
}
impl_astnode!(NodeMixin);
impl_astnode_displays!(NodeMixin);

pub struct NodeArrayExpression<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    members: Vec<&'a dyn AstNode<'a>>,
    is_dictionary: bool,
}
impl<'a> NodeArrayExpression<'a> {
    pub fn new(members: Vec<&'a dyn AstNode<'a>>, token: &'a LexerToken, is_dictionary: bool) -> NodeArrayExpression<'a> {
        return NodeArrayExpression {
            ty: NodeType::ArrayExpression,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            members: members,
            is_dictionary: is_dictionary
        }
    }
}
impl_astnode!(NodeArrayExpression);
impl_astnode_displays!(NodeArrayExpression);

pub struct NodeObjectExpression<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    members: Vec<&'a NodeDeclare<'a>>,
}
impl<'a> NodeObjectExpression<'a> {
    pub fn new(members: Vec<&'a NodeDeclare<'a>>) -> NodeObjectExpression<'a> {
        return NodeObjectExpression {
            // Members are var decls
            ty: NodeType::ObjectExpression,
            tok: None,
            loc: (0, 0),

            members: members
        }
    }
}
impl_astnode!(NodeObjectExpression);
impl_astnode_displays!(NodeObjectExpression);

pub struct NodeMemberExpression<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    lhs: &'a dyn AstNode<'a>,
    identifier: &'a LexerToken,
}
impl<'a> NodeMemberExpression<'a> {
    pub fn new(lhs: &'a dyn AstNode<'a>, identifier: &'a LexerToken, token: &'a LexerToken) -> NodeMemberExpression<'a> {
        return NodeMemberExpression {
            ty: NodeType::MemberExpression,
            tok: Some(NodeTokenType::Token(token)),
            loc: token.location,

            lhs: lhs,
            identifier: identifier
        }
    }
}
impl_astnode!(NodeMemberExpression);
impl_astnode_displays!(NodeMemberExpression);

pub struct NodeArrayAccessExpression<'a> {
    ty: NodeType,
    tok: Option<NodeTokenType<'a>>,
    loc: (i32, i32),

    lhs: &'a dyn AstNode<'a>,
    access_expr: &'a dyn AstNode<'a>,
}
impl<'a> NodeArrayAccessExpression<'a> {
    pub fn new(lhs: &'a dyn AstNode<'a>, access_expr: &'a dyn AstNode<'a>, token: &'a LexerToken) -> NodeArrayAccessExpression<'a> {
        return NodeArrayAccessExpression {
            ty: NodeType::ArrayAccessExpression,
            tok: Some(NodeTokenType::Token(token)),
            loc: (0, 0),

            lhs: lhs,
            access_expr: access_expr
        }
    }
}
impl_astnode!(NodeArrayAccessExpression);
impl_astnode_displays!(NodeArrayAccessExpression);
