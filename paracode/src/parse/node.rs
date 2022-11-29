use std::fmt;
use std::convert::AsRef;

use strum_macros::AsRefStr;

use crate::lexer::LexerToken;
use crate::lexer::TokenType;

#[derive(PartialEq, Debug, Clone)]
pub enum NumberType {
    Int(i32),
    Float(f32),
}

#[derive(Eq, PartialEq, Debug, EnumString, strum_macros::Display, AsRefStr)]
pub enum NodeType {
    #[strum(serialize="Empty", serialize="0")]
    Empty,
    #[strum(serialize="BinOp", serialize="1")]
    BinOp,
    #[strum(serialize="Number", serialize="2")]
    Number,
    #[strum(serialize="String", serialize="3")]
    String,
    #[strum(serialize="UnaryOp", serialize="4")]
    UnaryOp,
    #[strum(serialize="Block", serialize="5")]
    Block,
    #[strum(serialize="Assign", serialize="6")]
    Assign,
    #[strum(serialize="Variable", serialize="7")]
    Variable,
    #[strum(serialize="Type", serialize="8")]
    Type,
    #[strum(serialize="Declare", serialize="9")]
    Declare,
    #[strum(serialize="Call", serialize="10")]
    Call,
    #[strum(serialize="Import", serialize="11")]
    Import,
    #[strum(serialize="While", serialize="12")]
    While,
    #[strum(serialize="For", serialize="13")]
    For,
    #[strum(serialize="IfStatement", serialize="14")]
    IfStatement,
    #[strum(serialize="Try", serialize="15")]
    Try,
    #[strum(serialize="ArgumentList", serialize="16")]
    ArgumentList,
    #[strum(serialize="SplatArgument", serialize="17")]
    SplatArgument,
    #[strum(serialize="FunctionReturn", serialize="18")]
    FunctionReturn,
    #[strum(serialize="FunctionExpression", serialize="19")]
    FunctionExpression,
    #[strum(serialize="Macro", serialize="20")]
    Macro,
    #[strum(serialize="Mixin", serialize="21")]
    Mixin,
    #[strum(serialize="ArrayExpression", serialize="22")]
    ArrayExpression,
    #[strum(serialize="ObjectExpression", serialize="23")]
    ObjectExpression,
    #[strum(serialize="MemberExpression", serialize="24")]
    MemberExpression,
    #[strum(serialize="ArrayAccessExpression", serialize="25")]
    ArrayAccessExpression
}

pub trait AstNode<'a>: fmt::Display {
    fn node_type(&self) -> &NodeType;
    fn token(&self) -> Option<&'a LexerToken>;
    fn location(&self) -> Option<(i32, i32)>;
}

#[macro_export]
macro_rules! impl_astnode_base {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl<'a> AstNode<'a> for $name<'a> {
            fn node_type(&self) -> &NodeType {
                return &self.ty;
            }
            
            fn token(&self) -> Option<&'a LexerToken> {
                return self.tok;
            }

            fn location(&self) -> Option<(i32, i32)> {
                return self.loc;
            }
        }
    };
}
#[macro_export]
macro_rules! impl_astnode {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl_astnode_base!($name);
        impl<'a> std::fmt::Display for $name<'a> {
            fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
                return match self.token() {
                    Some(tok) => write!(f, "AstNode[{}, {}]", self.node_type().as_ref(), tok),
                    None => write!(f, "AstNode[{}]", self.node_type().as_ref()),
                }
            }
        }
    };
}

pub struct NodeNone<'a> {
    ty: NodeType,
    tok: Option<&'a LexerToken>,
    loc: Option<(i32, i32)>,
}
impl<'a> NodeNone<'a> {
    pub fn new(token: &'a LexerToken) -> NodeNone<'a> {
        return NodeNone {
            ty: NodeType::Empty,
            tok: Some(token),
            loc: Some(token.location)
        }
    }
}
impl_astnode!(NodeNone);

// Binary op node; LEFT [+-*/] RIGHT
pub struct NodeBinOp<'a> {
    ty: NodeType,
    tok: Option<&'a LexerToken>,
    loc: Option<(i32, i32)>,

    left: &'a dyn AstNode<'a>,
    right: &'a dyn AstNode<'a>,
}
impl<'a> NodeBinOp<'a> {
    pub fn new(left: &'a dyn AstNode<'a>, token: &'a LexerToken, right: &'a dyn AstNode<'a>) -> NodeBinOp<'a> {
        return NodeBinOp {
            ty: NodeType::BinOp,
            tok: Some(token),
            loc: Some(token.location),

            left: left,
            right: right
        }
    }
}
impl_astnode!(NodeBinOp);

pub struct NodeNumber<'a> {
    ty: NodeType,
    tok: Option<&'a LexerToken>,
    loc: Option<(i32, i32)>,

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
            tok: Some(token),
            loc: Some(token.location),

            value: value
        }
    }
}
impl_astnode!(NodeNumber);

pub struct NodeString<'a> {
    ty: NodeType,
    tok: Option<&'a LexerToken>,
    loc: Option<(i32, i32)>,

    value: String,
}
impl<'a> NodeString<'a> {
    pub fn new(token: &'a LexerToken) -> NodeString<'a> {
        return NodeString {
            ty: NodeType::String,
            tok: Some(token),
            loc: Some(token.location),

            value: token.value[1..token.value.len() - 1].to_string()
        }
    }
}
impl_astnode!(NodeString);
