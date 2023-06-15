use std::convert::AsRef;
use std::fmt;

use strum_macros::AsRefStr;
use dyn_clone::{clone_trait_object, DynClone};

use crate::lexer::LexerToken;
use crate::parse::source_location::SourceLocation;

#[derive(PartialEq, Debug, Clone)]
pub enum NumberType {
    Int(i32),
    Float(f32),
}

#[derive(Debug, Clone)]
pub enum NodeValueType {
    Number(NumberType),
    String(String),
    Node(Box<dyn AstNode>),
}

#[derive(Debug, Clone)]
pub enum NodeOrVec {
    Node(Box<dyn AstNode>),
    Vec(Vec<Box<dyn AstNode>>),
}

#[derive(Eq, PartialEq, Debug, Clone, EnumString, strum_macros::Display, AsRefStr)]
pub enum NodeType {
    #[strum(serialize = "Empty", serialize = "1")]
    Empty,
    #[strum(serialize = "BinOp", serialize = "2")]
    BinOp,
    #[strum(serialize = "Number", serialize = "3")]
    Number,
    #[strum(serialize = "String", serialize = "4")]
    String,
    #[strum(serialize = "UnaryOp", serialize = "5")]
    UnaryOp,
    #[strum(serialize = "Block", serialize = "6")]
    Block,
    #[strum(serialize = "Assign", serialize = "7")]
    Assign,
    #[strum(serialize = "Variable", serialize = "8")]
    Variable,
    #[strum(serialize = "Type", serialize = "9")]
    Type,
    #[strum(serialize = "Declare", serialize = "10")]
    Declare,
    #[strum(serialize = "Call", serialize = "11")]
    Call,
    #[strum(serialize = "Import", serialize = "12")]
    Import,
    #[strum(serialize = "While", serialize = "13")]
    While,
    #[strum(serialize = "For", serialize = "14")]
    For,
    #[strum(serialize = "IfStatement", serialize = "15")]
    IfStatement,
    #[strum(serialize = "Try", serialize = "16")]
    Try,
    #[strum(serialize = "ArgumentList", serialize = "17")]
    ArgumentList,
    #[strum(serialize = "SplatArgument", serialize = "18")]
    SplatArgument,
    #[strum(serialize = "FunctionReturn", serialize = "19")]
    FunctionReturn,
    #[strum(serialize = "FunctionExpression", serialize = "20")]
    FunctionExpression,
    #[strum(serialize = "Macro", serialize = "21")]
    Macro,
    #[strum(serialize = "Mixin", serialize = "22")]
    Mixin,
    #[strum(serialize = "ArrayExpression", serialize = "23")]
    ArrayExpression,
    #[strum(serialize = "ObjectExpression", serialize = "24")]
    ObjectExpression,
    #[strum(serialize = "MemberExpression", serialize = "25")]
    MemberExpression,
    #[strum(serialize = "ArrayAccessExpression", serialize = "26")]
    ArrayAccessExpression,
}

#[derive(Clone)]
pub enum NodeTokenType {
    Token(LexerToken),
    Node(Box<dyn AstNode>),
}
impl fmt::Display for NodeTokenType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return match self {
            NodeTokenType::Token(tok) => write!(f, "{}", tok),
            NodeTokenType::Node(node) => write!(f, "{}", node),
        };
    }
}
impl fmt::Debug for NodeTokenType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return match self {
            NodeTokenType::Token(tok) => write!(f, "{:?}", tok),
            NodeTokenType::Node(node) => write!(f, "{:?}", node),
        };
    }
}

pub trait AstNode: fmt::Debug + fmt::Display + DynClone {
    fn node_type(&self) -> NodeType;
    fn token(&self) -> Option<NodeTokenType>;
    fn location(&self) -> (i32, i32);
    fn is_splat(&self) -> bool;   
    fn get_value(&self) -> Option<NodeValueType>;

    fn as_dyn(&self) -> Box<dyn AstNode>;
}
clone_trait_object!(AstNode);

#[macro_export]
macro_rules! impl_astnode_displays {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl std::fmt::Display for $name {
            fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
                return match self.token() {
                    Some(tok) => write!(f, "AstNode[{}, {}]", self.node_type().as_ref(), tok),
                    None => write!(f, "AstNode[{}]", self.node_type().as_ref()),
                };
            }
        }
        impl std::fmt::Debug for $name {
            fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
                return write!(f, "{}", self);
            }
        }
    };
}

#[derive(Clone)]
pub struct NodeNone {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),
}
impl NodeNone {
    pub fn new(token: LexerToken) -> NodeNone {
        return NodeNone {
            ty: NodeType::Empty,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,
        };
    }
}
impl AstNode for NodeNone {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeNone);

// Binary op node; LEFT [+-*/] RIGHT
#[derive(Clone)]
pub struct NodeBinOp {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    left: Box<dyn AstNode>,
    right: Box<dyn AstNode>,
}
impl NodeBinOp {
    pub fn new(
        left: Box<dyn AstNode>,
        token: LexerToken,
        right: Box<dyn AstNode>,
    ) -> NodeBinOp {
        return NodeBinOp {
            ty: NodeType::BinOp,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            left: left,
            right: right,
        };
    }
}
impl AstNode for NodeBinOp {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeBinOp);

#[derive(Clone)]
pub struct NodeNumber {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    value: NumberType,
}
impl NodeNumber {
    pub fn new(token: LexerToken) -> NodeNumber {
        let value: NumberType;
        if token.value.contains(".") {
            value = NumberType::Float(lexical::parse::<f32, _>(&token.value).unwrap());
        } else {
            value = NumberType::Int(lexical::parse::<i32, _>(&token.value).unwrap());
        }
        return NodeNumber {
            ty: NodeType::Number,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            value: value,
        };
    }
}
impl AstNode for NodeNumber {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return Some(NodeValueType::Number(self.value.clone()));
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeNumber);

#[derive(Clone)]
pub struct NodeString {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    value: String,
}
impl NodeString {
    pub fn new(token: LexerToken) -> NodeString {
        return NodeString {
            ty: NodeType::String,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            value: token.value[1..token.value.len() - 1].to_string(),
        };
    }
}
impl AstNode for NodeString {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return Some(NodeValueType::String(self.value.clone()));
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeString);

// Unary node; switches signage for values, '!' operator
#[derive(Clone)]
pub struct NodeUnaryOp {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    expression: Box<dyn AstNode>,
}
impl NodeUnaryOp {
    pub fn new(token: LexerToken, expression: Box<dyn AstNode>) -> NodeUnaryOp {
        return NodeUnaryOp {
            ty: NodeType::UnaryOp,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            expression: expression,
        };
    }
}
impl AstNode for NodeUnaryOp {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeUnaryOp);

// Block node; parent to multiple nodes
#[derive(Clone)]
pub struct NodeBlock {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    pub children: Vec<Box<dyn AstNode>>,
}
impl NodeBlock {
    pub fn new(token: LexerToken) -> NodeBlock {
        return NodeBlock {
            ty: NodeType::Block,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            children: vec![],
        };
    }
}
impl AstNode for NodeBlock {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeBlock);

// Type node; Holds type info for variable
#[derive(Clone)]
pub struct NodeVarType {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),
}
impl NodeVarType {
    pub fn new(token: LexerToken) -> NodeVarType {
        return NodeVarType {
            ty: NodeType::Type,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,
        };
    }

    pub fn is_type_type(&self) -> bool {
        return match self.tok.as_ref().unwrap() {
            NodeTokenType::Token(tok) => tok.value == "type",
            NodeTokenType::Node(_) => unreachable!(),
        };
    }
}
impl AstNode for NodeVarType {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeVarType);

// Declare node; declare variable or function
#[derive(Clone)]
pub struct NodeDeclare {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    type_node: Option<Box<dyn AstNode>>,
    name: LexerToken,
    value: Box<dyn AstNode>,
    allow_casting: bool,
}
impl NodeDeclare {
    pub fn new(
        ty: Option<Box<dyn AstNode>>,
        name: LexerToken,
        value: Box<dyn AstNode>,
        allow_casting: bool,
    ) -> NodeDeclare {
        return NodeDeclare {
            ty: NodeType::Declare,
            tok: Some(NodeTokenType::Token(name.clone())),
            loc: name.location,

            type_node: ty,
            name: name,
            value: value,
            allow_casting: allow_casting,
        };
    }
}
impl AstNode for NodeDeclare {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }
    
    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }
    
    fn location(&self) -> (i32, i32) {
        return self.loc;
    }
    
    fn is_splat(&self) -> bool {
        return false;
    }
    
    fn get_value(&self) -> Option<NodeValueType> {
        return Some(NodeValueType::Node(self.value.clone()));
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeDeclare);

#[derive(Clone)]
pub struct NodeImport {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    pub children: Vec<Box<dyn AstNode>>,
    source_location: SourceLocation,
}
impl NodeImport {
    pub fn new(filename: LexerToken, source_location: SourceLocation) -> NodeImport {
        return NodeImport {
            ty: NodeType::Import,
            tok: Some(NodeTokenType::Token(filename.clone())),
            loc: filename.location,

            children: vec![],
            source_location: source_location,
        };
    }
}
impl AstNode for NodeImport {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeImport);

#[derive(Clone)]
pub struct NodeWhile {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    block: NodeBlock,
    expr: Box<dyn AstNode>,
}
impl NodeWhile {
    pub fn new(
        expr: Box<dyn AstNode>,
        block: NodeBlock,
        token: LexerToken,
    ) -> NodeWhile {
        return NodeWhile {
            ty: NodeType::While,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            block: block,
            expr: expr,
        };
    }
}
impl AstNode for NodeWhile {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeWhile);

#[derive(Clone)]
pub struct NodeFor {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    var_token: LexerToken,
    block: NodeBlock,
    expr: Box<dyn AstNode>,
}
impl NodeFor {
    pub fn new(
        var_token: LexerToken,
        expr: Box<dyn AstNode>,
        block: NodeBlock,
        token: LexerToken,
    ) -> NodeFor {
        return NodeFor {
            ty: NodeType::For,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            var_token: var_token,
            block: block,
            expr: expr,
        };
    }
}
impl AstNode for NodeFor {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeFor);

#[derive(Clone)]
pub struct NodeCall {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    lhs: Box<dyn AstNode>,
    argument_list: NodeArgumentList,
}
impl NodeCall {
    pub fn new(lhs: Box<dyn AstNode>, argument_list: NodeArgumentList) -> NodeCall {
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
            argument_list: argument_list,
        };
    }
}
impl AstNode for NodeCall {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeCall);

// Assignment node; Var = Value
#[derive(Clone)]
pub struct NodeAssign {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    lhs: Box<dyn AstNode>,
    pub value: Box<dyn AstNode>,
}
impl NodeAssign {
    pub fn new(lhs: Box<dyn AstNode>, value: Box<dyn AstNode>) -> NodeAssign {
        return NodeAssign {
            ty: NodeType::Assign,
            tok: Some(NodeTokenType::Node(value.clone())),
            loc: value.location(),

            lhs: lhs,
            value: value,
        };
    }
}
impl AstNode for NodeAssign {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }
    
    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }
    
    fn location(&self) -> (i32, i32) {
        return self.loc;
    }
    
    fn is_splat(&self) -> bool {
        return false;
    }
    
    fn get_value(&self) -> Option<NodeValueType> {
        return Some(NodeValueType::Node(self.value.clone()));
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeAssign);

// Variable node; request value of variable
#[derive(Clone)]
pub struct NodeVariable {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    value: String,
    allow_casting: bool,
}
impl NodeVariable {
    pub fn new(token: LexerToken, allow_casting: bool) -> NodeVariable {
        return NodeVariable {
            ty: NodeType::Variable,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            value: token.value,
            allow_casting: allow_casting,
        };
    }
}
impl AstNode for NodeVariable {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return Some(NodeValueType::String(self.value.clone()));
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeVariable);

#[derive(Clone)]
pub struct NodeIfStatement {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    expr: Box<dyn AstNode>,
    block: NodeBlock,
    else_block: Option<Box<dyn AstNode>>,
}
impl NodeIfStatement {
    pub fn new(
        expr: Box<dyn AstNode>,
        block: NodeBlock,
        else_block: Option<Box<dyn AstNode>>,
        token: LexerToken,
    ) -> NodeIfStatement {
        return NodeIfStatement {
            ty: NodeType::IfStatement,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            expr: expr,
            block: block,
            else_block: else_block,
        };
    }
}
impl AstNode for NodeIfStatement {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeIfStatement);

#[derive(Clone)]
pub struct NodeTryCatch {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    block: NodeBlock,
    catch_block: Vec<NodeBlock>,
    expr: Vec<NodeOrVec>,
    else_block: Option<Box<dyn AstNode>>,
    finally_block: Option<Box<dyn AstNode>>,
    variable: Vec<Option<NodeDeclare>>,
}
impl NodeTryCatch {
    pub fn new(
        block: NodeBlock,
        catch_block: Vec<NodeBlock>,
        expr: Vec<NodeOrVec>,
        else_block: Option<Box<dyn AstNode>>,
        finally_block: Option<Box<dyn AstNode>>,
        token: LexerToken,
        variable: Vec<Option<NodeDeclare>>,
    ) -> NodeTryCatch {
        return NodeTryCatch {
            ty: NodeType::Try,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            block: block,
            catch_block: catch_block,
            expr: expr,
            else_block: else_block,
            finally_block: finally_block,
            variable: variable,
        };
    }
}
impl AstNode for NodeTryCatch {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeTryCatch);

#[derive(Clone)]
pub struct NodeArgumentList {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    pub arguments: Vec<NodeTokenType>,
}
impl NodeArgumentList {
    pub fn new(arguments: Vec<NodeTokenType>, token: Option<NodeTokenType>) -> NodeArgumentList {
        return NodeArgumentList {
            ty: NodeType::ArgumentList,
            tok: token.clone(),
            loc: match token {
                Some(t) => match t {
                    NodeTokenType::Token(tok) => tok.location,
                    NodeTokenType::Node(node) => node.location(),
                },
                None => (0, 0),
            },

            arguments: arguments,
        };
    }
}
impl AstNode for NodeArgumentList {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeArgumentList);

#[derive(Clone)]
pub struct NodeSplatArgument {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    expr: Box<dyn AstNode>,
}
impl NodeSplatArgument {
    pub fn new(expr: Box<dyn AstNode>, token: LexerToken) -> NodeSplatArgument {
        return NodeSplatArgument {
            ty: NodeType::SplatArgument,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            expr: expr,
        };
    }
}
impl AstNode for NodeSplatArgument {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return true;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeSplatArgument);

#[derive(Clone)]
pub struct NodeFunctionExpression {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    block: NodeBlock,
    argument_list: NodeArgumentList,
}
impl NodeFunctionExpression {
    pub fn new(
        argument_list: NodeArgumentList,
        block: NodeBlock,
    ) -> NodeFunctionExpression {
        return NodeFunctionExpression {
            ty: NodeType::FunctionExpression,
            tok: Some(NodeTokenType::Node(Box::new(block.clone()))),
            loc: block.location(),

            block: block,
            argument_list: argument_list,
        };
    }
}
impl AstNode for NodeFunctionExpression {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeFunctionExpression);

#[derive(Clone)]
pub struct NodeFunctionReturn {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    value_node: Box<dyn AstNode>,
}
impl NodeFunctionReturn {
    pub fn new(value_node: Box<dyn AstNode>, token: Option<NodeTokenType>) -> NodeFunctionReturn {
        return NodeFunctionReturn {
            ty: NodeType::FunctionReturn,
            tok: token.clone(),
            loc: match token {
                Some(t) => match t {
                    NodeTokenType::Token(tok) => tok.location,
                    NodeTokenType::Node(node) => node.location(),
                },
                None => (0, 0),
            },

            value_node: value_node,
        };
    }
}
impl AstNode for NodeFunctionReturn {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeFunctionReturn);

#[derive(Clone)]
pub struct NodeMacro {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    expr: NodeCall,
}
impl NodeMacro {
    pub fn new(expr: NodeCall, token: LexerToken) -> NodeMacro {
        return NodeMacro {
            ty: NodeType::Macro,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            expr: expr,
        };
    }
}
impl AstNode for NodeMacro {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeMacro);

#[derive(Clone)]
pub struct NodeMixin {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    tokens: Vec<LexerToken>,
}
impl NodeMixin {
    pub fn new(tokens: Vec<LexerToken>, token: LexerToken) -> NodeMixin {
        return NodeMixin {
            ty: NodeType::Mixin,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            tokens: tokens,
        };
    }
}
impl AstNode for NodeMixin {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeMixin);

#[derive(Clone)]
pub struct NodeArrayExpression {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    members: Vec<Box<dyn AstNode>>,
    is_dictionary: bool,
}
impl NodeArrayExpression {
    pub fn new(
        members: Vec<Box<dyn AstNode>>,
        token: LexerToken,
        is_dictionary: bool,
    ) -> NodeArrayExpression {
        return NodeArrayExpression {
            ty: NodeType::ArrayExpression,
            tok: Some(NodeTokenType::Token(token.clone())),
            loc: token.location,

            members: members,
            is_dictionary: is_dictionary,
        };
    }
}
impl AstNode for NodeArrayExpression {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeArrayExpression);

#[derive(Clone)]
pub struct NodeObjectExpression {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    members: Vec<NodeDeclare>,
}
impl NodeObjectExpression {
    pub fn new(members: Vec<NodeDeclare>) -> NodeObjectExpression {
        return NodeObjectExpression {
            // Members are var decls
            ty: NodeType::ObjectExpression,
            tok: None,
            loc: (0, 0),

            members: members,
        };
    }
}
impl AstNode for NodeObjectExpression {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeObjectExpression);

#[derive(Clone)]
pub struct NodeMemberExpression {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    lhs: Box<dyn AstNode>,
    identifier: LexerToken,
}
impl NodeMemberExpression {
    pub fn new(
        lhs: Box<dyn AstNode>,
        identifier: LexerToken,
        token: Option<NodeTokenType>,
    ) -> NodeMemberExpression {
        return NodeMemberExpression {
            ty: NodeType::MemberExpression,
            tok: token.clone(),
            loc: match token {
                Some(t) => match t {
                    NodeTokenType::Token(tok) => tok.location,
                    NodeTokenType::Node(node) => node.location(),
                },
                None => (0, 0),
            },

            lhs: lhs,
            identifier: identifier,
        };
    }
}
impl AstNode for NodeMemberExpression {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeMemberExpression);

#[derive(Clone)]
pub struct NodeArrayAccessExpression {
    ty: NodeType,
    tok: Option<NodeTokenType>,
    loc: (i32, i32),

    lhs: Box<dyn AstNode>,
    access_expr: Box<dyn AstNode>,
}
impl NodeArrayAccessExpression {
    pub fn new(
        lhs: Box<dyn AstNode>,
        access_expr: Box<dyn AstNode>,
        token: LexerToken,
    ) -> NodeArrayAccessExpression {
        return NodeArrayAccessExpression {
            ty: NodeType::ArrayAccessExpression,
            tok: Some(NodeTokenType::Token(token)),
            loc: (0, 0),

            lhs: lhs,
            access_expr: access_expr,
        };
    }
}
impl AstNode for NodeArrayAccessExpression {
    fn node_type(&self) -> NodeType {
        return self.ty.clone();
    }

    fn token(&self) -> Option<NodeTokenType> {
        return self.tok.clone();
    }

    fn location(&self) -> (i32, i32) {
        return self.loc;
    }

    fn is_splat(&self) -> bool {
        return false;
    }

    fn get_value(&self) -> Option<NodeValueType> {
        return None;
    }

    fn as_dyn(&self) -> Box<dyn AstNode> {
        Box::new(self.clone())
    }
}
impl_astnode_displays!(NodeArrayAccessExpression);
