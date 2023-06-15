use std::fs;
use std::str::FromStr;

use crate::lexer::Keywords;
use crate::lexer::TokenType;
use crate::lexer::LexerToken;
use crate::lexer::Lexer;
use crate::parse::node::AstNode;
use crate::parse::source_location::SourceLocation;
use crate::parse::node::*;
use crate::error::ErrorType;
use crate::error::Error;
use crate::error::ErrorList;

pub struct Parser {
    tokens: Vec<Option<LexerToken>>,
    token_index: i32,
    current_tok: Option<LexerToken>,
    pub error_list: ErrorList,

    source_location: SourceLocation,
}
impl Parser {
    pub fn new(tokens: Vec<Option<LexerToken>>, source_location: SourceLocation) -> Parser {
        let mut parser = Parser {
            tokens: tokens,
            token_index: 0,
            current_tok: None,
            error_list: ErrorList::new(),

            source_location: source_location
        };
        parser.current_tok = parser.next_tok();
        return parser;
    }

    pub fn filename(&self) -> &String {
        return &self.source_location.filename;
    }

    pub fn current_token(&self) -> LexerToken {
        if self.current_tok.is_none() {
            return LexerToken::none().clone();
        }
        return self.current_tok.clone().unwrap();
    }

    pub fn expect_token(&mut self, token_type: TokenType, offset: i32, tok: Option<LexerToken>) -> Option<LexerToken> {
        let token = match tok {
            Some(t) => Some(t),
            // If no token passed in, peek from offset
            None => self.peek_token(offset, None),
        };

        // You'd think the borrow checker would be smart enough to
        // let this work without having to use a variable for Some(token_type).
        let some_token_type = Some(token_type);
        // TODO: Handle token if it is None
        if token.clone().unwrap().token_type == some_token_type {
            return token;
        }
        else {
            self.error(format!("expected {:?} but recieved {:?}", some_token_type, token.unwrap().token_type));
            return None;
        }
    }

    pub fn next_tok(&mut self) -> Option<LexerToken> {
        // Check if next index is past list boundaries
        if (self.token_index + 1) as usize > self.tokens.len() {
            return None;
        }
        
        // Return selected token, increment index
        self.current_tok = self.tokens[self.token_index as usize].clone();
        self.token_index += 1;
        
        return self.current_tok.clone();
    }
    
    pub fn next_token(&mut self) -> Option<LexerToken> {
        // Check if next index is past list boundaries
        if (self.token_index + 1) as usize > self.tokens.len() {
            return None;
        }
        
        // Return selected token, increment index
        self.current_tok = self.tokens[self.token_index as usize].clone();
        self.token_index += 1;
        
        return Some(self.current_token());
    }

    // Return token at token.index + offset
    pub fn peek_token(&self, offset: i32, expected_type: Option<TokenType>) -> Option<LexerToken> {
        // Check bounds
        if (self.token_index + offset - 1) as usize > self.tokens.len() {
            return None;
        }
            
        let token = &self.tokens[(self.token_index + offset - 1) as usize];
        
        if expected_type.is_some() && token.is_some() && token.clone().unwrap().token_type != expected_type {
            return None;
        }
        
        return token.clone();
    }

    pub fn error(&mut self, message: String) {
        // Tokens have locations attached from the lexer, pass to self.error
        // if an error occurs
        let location = self.current_token().location;

        self.error_list.push_error(Error::new(ErrorType::Syntax, location, message, self.filename().clone(), "Syntax Error".to_string()));
    }

    // Read next token and error if token.type != passed in token type
    pub fn eat(&mut self, token_type: Option<TokenType>) -> Option<LexerToken> {
        if token_type.is_some() {
            if self.expect_token(token_type.unwrap(), 0, None).is_none() {
                return None;
            }
        }

        self.current_tok = self.next_tok();

        return Some(self.current_token());
    }

    // Parse reference to a variable
    pub fn parse_variable(&mut self) -> NodeVariable {
        // Create variable node and eat identifier
        let variable_node = NodeVariable::new(self.current_token(), false);

        self.eat(Some(TokenType::Identifier));
        
        return variable_node;
    }

    pub fn parse_member_expression(&mut self, lhs: Box<dyn AstNode>) -> Result<NodeMemberExpression, Option<String>> {
        if self.eat(Some(TokenType::Dot)).is_none() {
            return Err(None);
        }

        let token = self.current_token();

        // Expect identifier for right hand side
        let rhs_name = self.peek_token(0, Some(TokenType::Identifier));

        if rhs_name.is_none() {
            self.error("invalid member access: must be in format <expression>.<identifier>".to_string());
            return Err(None);
        }

        self.eat(Some(TokenType::Identifier));

        return Ok(NodeMemberExpression::new(lhs, rhs_name.unwrap(), Some(NodeTokenType::Token(token))));
    }

    pub fn parse_array_access_expression(&mut self, lhs: Box<dyn AstNode>) -> Result<NodeArrayAccessExpression, Option<String>> {
        if self.eat(Some(TokenType::LBracket)).is_none() {
            return Err(None);
        }

        let token = self.current_token();

        // Get internal expr
        let access_expr = self.parse_expression();

        if access_expr.is_err() {
            self.error("invalid array access expression".to_string());
            return Err(access_expr.unwrap_err());
        }

        if self.eat(Some(TokenType::RBracket)).is_none() {
            return Err(None);
        }

        return Ok(NodeArrayAccessExpression::new(lhs, access_expr.unwrap(), token));
    }
    
    pub fn import_file(&mut self, filename: String, filename_token: Option<LexerToken>) -> Result<NodeImport, Option<String>> {
        let data = match fs::read_to_string(filename.clone()) {
            Ok(data) => data,
            Err(_) => {
                self.error(format!("source file '{}' does not exist", filename).to_string());
                return Err(None);
            }
        };

        let source_location = SourceLocation::new(filename.clone(), 1, 1);

        let mut lexer = Lexer::new(&data, source_location.clone());
        let tokens = lexer.lex()?;
        
        let mut parser = Parser::new(tokens, source_location.clone());
        
        // An import node acts similar to a block and holds all variables and functions
        // in a tree. A parser is passed for getting various information in the interpreter
        let filename_tok = filename_token.unwrap_or(LexerToken::new(format!("\"{}\"", filename).to_string(), None));
        
        let mut node = NodeImport::new(filename_tok, source_location);
        node.children = parser.get_statements()?;

        for error in parser.error_list.errors.iter() {
            self.error_list.push_error(error.clone());
        }
        
        return Ok(node);
    }
    
    pub fn parse_while(&mut self) -> Result<NodeWhile, Option<String>> {
        // Eat while keyword
        let token = self.current_token();
        if self.eat(Some(TokenType::Keyword)).is_none() {
            return Err(None);
        }

        let expression = self.parse_expression()?;

        let block = self.parse_block_statement()?;
        
        return Ok(NodeWhile::new(expression, block, token));
    }

    pub fn parse_for(&mut self) -> Result<NodeFor, Option<String>> {
        // Eat for keyword
        let token = self.current_token();
        if self.eat(Some(TokenType::Keyword)).is_none() {
            return Err(None);
        }

        // Get var name of iter
        let var_token = self.current_token();
        self.eat(Some(TokenType::Identifier));
        if var_token.is_none() {
            return Err(None);
        }

        // Eat in keyword
        let in_keyword = self.current_token();
        self.eat(Some(TokenType::Keyword));
        if in_keyword.is_none() || in_keyword.value != "in" {
            self.error("for loop expects syntax `for <var> in <expr> { ... }`".to_string());
            return Err(None);
        }

        let expression = self.parse_expression()?;

        let block = self.parse_block_statement()?;

        return Ok(NodeFor::new(var_token, expression, block, token));
    }

    pub fn parse_macro(&mut self) -> Result<NodeDeclare, Option<String>> {
        let token = self.current_token();
        self.eat(Some(TokenType::Keyword));

        // Eat macro name
        let name = self.current_token();
        if self.eat(Some(TokenType::Identifier)).is_none() {
            return Err(None);
        }

        let mut argument_list = None;
        
        // Eat optional arguments
        if self.peek_token(0, Some(TokenType::LParen)).is_some() {
            argument_list = Some(self.parse_argument_list()?);

            if argument_list.is_none() {
                return Err(None);
            }
        }

        // Parse block
        let block = self.parse_block_statement()?;

        // Add self argument
        let macro_self_argument = Box::new(NodeDeclare::new(None, LexerToken::new("__macro_self".to_string(), Some(TokenType::Identifier)), Box::new(NodeNone::new(token.clone())), false));

        if argument_list.is_none() {
            argument_list = Some(NodeArgumentList::new(
                vec![NodeTokenType::Node(macro_self_argument)],
                Some(NodeTokenType::Token(token.clone()))
            ));
        } else {
            let mut arg_list = argument_list.clone().unwrap();
            arg_list.arguments = vec![vec![NodeTokenType::Node(macro_self_argument)], arg_list.arguments].into_iter().flatten().collect();
        }

        let fun_expr = Box::new(NodeFunctionExpression::new(argument_list.unwrap(), block));
        
        let macro_var = Box::new(NodeVariable::new(LexerToken::new("Macro".to_string(), Some(TokenType::Identifier)), false));

        let member_access_call_node = NodeCall::new(
            Box::new(NodeMemberExpression::new(
                macro_var.clone(),
                LexerToken::new("new".to_string(), Some(TokenType::Identifier)),
                macro_var.token().clone()
            )),
            NodeArgumentList::new(
                vec![NodeTokenType::Node(fun_expr)],
                macro_var.token().clone()
            )
        );
        
        // Parse assignment, parenthesis, etc.
        let val_node = Box::new(NodeAssign::new(Box::new(NodeVariable::new(name.clone(), false)), Box::new(NodeMacro::new(member_access_call_node, token))));
        let type_node = Box::new(NodeVariable::new(LexerToken::new("Macro".to_string(), Some(TokenType::Identifier)), false));
        let node = NodeDeclare::new(Some(type_node), name, val_node, false);
        
        return Ok(node);
    }

    pub fn parse_mixin(&mut self) -> Result<NodeMixin, Option<String>> {
        // TODO: Error if not in macro
        // Eat keyword
        let token = self.current_token().clone();
        self.eat(Some(TokenType::Keyword));

        // Eat tokens in block
        if self.eat(Some(TokenType::LBrace)).is_none() {
            return Err(None);
        }
    
        let mut tokens = vec![];
    
        let mut brace_level = 1;
    
        while brace_level > 0 && self.current_token().token_type != Some(TokenType::NoneToken) {
            if self.current_token().token_type == Some(TokenType::LBrace) {
                brace_level += 1;
            }
            else if self.current_token().token_type == Some(TokenType::RBrace) {
                brace_level -= 1;
            }
    
            tokens.push(self.current_token().clone());
    
            self.eat(None);
        }
    
        return Ok(NodeMixin::new(tokens, token));
    }

    pub fn parse_import(&mut self) -> Result<NodeImport, Option<String>> {
        self.eat(Some(TokenType::Keyword));
        
        let filename_token = self.current_token();
            
        self.expect_token(TokenType::String, 0, Some(filename_token.clone()));
        
        let mut filename = self.current_token().value[1..self.current_token().value.len()-1].to_string();
        let path = std::path::Path::new(&filename);
        if !path.exists() {
            let pkg_path = std::path::Path::new("pkg_data").join(path);
            if pkg_path.exists() {
                filename = pkg_path.to_str().unwrap().to_string();
            }
        }
        self.eat(Some(TokenType::String));
        return self.import_file(filename, Some(filename_token));
    }

    pub fn parse_return(&mut self) -> Result<NodeFunctionReturn, Option<String>> {
        self.eat(Some(TokenType::Keyword));
        let value_node = self.parse_expression()?;
        return Ok(NodeFunctionReturn::new(value_node, Some(NodeTokenType::Token(self.current_token()))));
    }

    pub fn parse_assignment_statement(&mut self, node: Box<dyn AstNode>, require_operator: bool) -> Result<NodeAssign, Option<String>> {
        // Operator would be '=' or '+=', '-=', etc.
        if require_operator {
            self.eat(None);
        }
    
        let value = self.parse_expression();
    
        if value.is_err() {
            self.error("Invalid assignment".to_string());
            return Err(value.unwrap_err());
        }
    
        let node = NodeAssign::new(node, value.unwrap());
        
        return Ok(node);
    }

    pub fn parse_argument_list(&mut self) -> Result<NodeArgumentList, Option<String>> {
        // Eat open parenthesis
        if self.eat(Some(TokenType::LParen)).is_none() {
            return Err(None);
        }

        let argument_list;

        if self.peek_token(0, Some(TokenType::RParen)).is_some() {
            argument_list = Some(NodeArgumentList::new(Vec::new(), Some(NodeTokenType::Token(self.current_token()))));
        } else {
            let mut arguments = Vec::new();
            let mut has_vargs = false;
            let mut first_arg = true;

            let mut any_default = false;

            loop {
                if has_vargs {
                    self.error("Arguments provided after variadic arguments".to_string());
                    break;
                }

                let mut is_vargs = false;

                if self.peek_token(0, Some(TokenType::Multiply)).is_some() {
                    is_vargs = true;
                    has_vargs = true;
                }

                let argument: Option<Box<dyn AstNode>>;

                if is_vargs {
                    // Eat *
                    if self.eat(Some(TokenType::Multiply)).is_none() {
                        return Err(None);
                    }

                    let token = self.current_token();
                    let var = self.parse_variable();

                    argument = Some(Box::new(NodeSplatArgument::new(Box::new(var), token)));
                } else {
                    if self.expect_token(TokenType::Identifier, 0, None).is_none() {
                        self.error("invalid argument format".to_string());
                        break;
                    }

                    // Parse declaration(vname:type) without let keyword
                    argument = Some(Box::new(self.parse_variable_declaration(false)?));
                }
                if argument.is_none() {
                    self.error("invalid argument".to_string());
                    break;
                }
                if let Some(arg) = argument.clone() {
                    if !arg.is_splat() && arg.get_value().is_some() {
                        any_default = true;
                    } else {
                        if any_default {
                            self.error("non-default argument follows default argument".to_string());
                            break;
                        }
                    }
                }
                arguments.push(NodeTokenType::Node(argument.unwrap()));

                if self.peek_token(0, Some(TokenType::Comma)).is_some() {
                    // Eat comma and continue on with argument list
                    self.eat(Some(TokenType::Comma));

                    first_arg = false;
                } else if !first_arg && self.peek_token(0, Some(TokenType::RParen)).is_none() && self.peek_token(1, Some(TokenType::LBrace)).is_none() {
                    // Not first arg and no comma, rollback?
                    break;
                } else {
                    break;
                }
            }
            argument_list = Some(NodeArgumentList::new(arguments, Some(NodeTokenType::Token(self.current_token()))));
        }
        
        if argument_list.is_none() {
            self.error("invalid argument list".to_string());
            return Err(None);
        }
        
        // Eat closing parenthesis
        self.eat(Some(TokenType::RParen));
            
        return Ok(argument_list.unwrap());
    }

    pub fn parse_parenthesis(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        // Eat open parenthesis
        self.eat(Some(TokenType::LParen));

        let expr = self.parse_expression()?;
        self.eat(Some(TokenType::RParen));

        return Ok(expr);
    }

    pub fn parse_statement(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        let token = self.current_token();

        if token.token_type == Some(TokenType::NoneToken) {
            return Err(Some("none".to_string()));
        }
        
        // Empty statement, eat semicolon and try again
        if token.token_type == Some(TokenType::Semicolon) {
            self.eat(Some(TokenType::Semicolon));
            return Ok(Box::new(NodeNone::new(token)));
        }

        let node;
            
        if token.token_type == Some(TokenType::Keyword) {
            node = Some(self.parse_keyword()?);
            
            if let Some(n) = node.clone() {
                // Check if node is function block, exempt from semicolon
                if n.node_type() == NodeType::Declare && n.get_value().is_some() {
                    match n.get_value().unwrap() {
                        NodeValueType::Number(_) => unreachable!(),
                        NodeValueType::String(_) => unreachable!(),
                        NodeValueType::Node(nv) => {
                            if nv.node_type() == NodeType::Assign && nv.get_value().is_some() {
                                match nv.get_value().unwrap() {
                                    NodeValueType::Number(_) => unreachable!(),
                                    NodeValueType::String(_) => unreachable!(),
                                    NodeValueType::Node(rhs) => {
                                        if rhs.node_type() == NodeType::FunctionExpression || rhs.node_type() == NodeType::Macro {
                                            return Ok(node.unwrap());
                                        }
                                    },
                                };
                            }
                        },
                    };
                }
            
                if n.node_type() == NodeType::IfStatement || n.node_type() == NodeType::Try || n.node_type() == NodeType::While || n.node_type() == NodeType::For || n.node_type() == NodeType::Mixin {
                    return Ok(node.unwrap());
                }
            }
        }
        else {
            let expr = self.parse_expression();

            if expr.is_err() {
                self.error(format!("Unknown token {:?} in statement", token.token_type));
                node = None;
            }
            else {
                node = Some(expr.unwrap());
            }
        }
        
        if self.current_token().token_type != Some(TokenType::Semicolon) {
            self.error(format!("Missing semicolon (found {})", match self.current_token().token_type {
                Some(t) => format!("{}", t),
                None => "None".to_string(),
            }));
        }
        else {
            // Eat semicolon at end of statement
            self.eat(Some(TokenType::Semicolon));
        }

        return match node {
            Some(n) => Ok(n),
            None => Err(None),
        }
    }

    pub fn get_statements(&mut self) -> Result<Vec<Box<dyn AstNode>>, Option<String>> {
        let mut statements = Vec::new();
        
        // Read until no statements left
        while !self.current_token().is_none() {
            // We hit last statement in block, break
            if self.current_token().token_type == Some(TokenType::RBrace) {
                break;
            }
                
            let statement = self.parse_statement()?;
            // Parse statement and skip to next semicolon
            statements.push(statement);
        }

        return Ok(statements);
    }

    pub fn parse_keyword(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        let keyword = self.expect_token(TokenType::Keyword, 0, None);

        if let Some(k) = keyword {
            if k.value == "let" {
                return Ok(Box::new(self.parse_variable_declaration(true)?));
            }
            else if k.value == "if" {
                return Ok(Box::new(self.parse_if_statement()?));
            }
            else if k.value == "func" {
                return Ok(Box::new(self.parse_func_declaration()?));
            }
            else if k.value == "import" {
                return Ok(Box::new(self.parse_import()?));
            }
            else if k.value == "return" {
                return Ok(Box::new(self.parse_return()?));
            }
            else if k.value == "while" {
                return Ok(Box::new(self.parse_while()?));
            }
            else if k.value == "for" {
                return Ok(Box::new(self.parse_for()?));
            }
            else if k.value == "macro" {
                return Ok(Box::new(self.parse_macro()?));
            }
            else if k.value == "mixin" {
                return Ok(Box::new(self.parse_mixin()?));
            }
            else if k.value == "try" {
                return Ok(Box::new(self.parse_try()?));
            }
            else {
                // TODO: Maybe add a system for extending this by also having a
                // list of extension handlers that return something specific
                self.error(format!("{:?} is not a valid keyword", k));
            }
        }
        else {
            self.error(format!("{:?} is not a valid keyword", keyword));
        }

        return Err(None);
    }

    pub fn parse_block_statement(&mut self) -> Result<NodeBlock, Option<String>> {
        self.eat(Some(TokenType::LBrace));
        let mut block = NodeBlock::new(self.current_token());
        block.children = self.get_statements()?;
        self.eat(Some(TokenType::RBrace));

        return Ok(block);
    }

    pub fn parse_array_expression(&mut self) -> Result<NodeArrayExpression, Option<String>> {
        let mut is_dictionary = false;
        let mut members = Vec::new();
        let mut left = Vec::new();
        let mut right = Vec::new();
    
        // Eat left bracket
        if self.eat(Some(TokenType::LBracket)).is_none() {
            return Err(None);
        }

        let mut token = self.current_token();

        let mut at_dictionary_value = false;

        if self.peek_token(0, Some(TokenType::Colon)).is_some() && self.peek_token(1, Some(TokenType::RBracket)).is_some() {
            is_dictionary = true;
            self.eat(Some(TokenType::Colon));
            token = self.current_token();
        }

        while token.token_type != Some(TokenType::RBracket) {
            // Parse expr
            let item_expr = self.parse_expression();

            if item_expr.is_err() {
                self.error(format!("Invalid array member item {:?}", self.current_token()));
                return Err(item_expr.unwrap_err());
            }

            if !is_dictionary && members.is_empty() && self.peek_token(0, Some(TokenType::Colon)).is_some() {
                is_dictionary = true;
            }
            
            if is_dictionary {
                if !at_dictionary_value {
                    left.push(item_expr.unwrap());
                }
                else {
                    right.push(item_expr.unwrap());
                }
            }
            else {
                members.push(item_expr.unwrap());
            }

            if self.current_token().token_type == Some(TokenType::Comma) {
                self.eat(Some(TokenType::Comma));
                if is_dictionary && at_dictionary_value {
                    at_dictionary_value = false;
                }
            }
            else if self.current_token().token_type == Some(TokenType::Colon) && is_dictionary && !at_dictionary_value {
                self.eat(Some(TokenType::Colon));
                at_dictionary_value = true;
            }
            else {
                break;
            }
        }

        if is_dictionary {
            members.push(Box::new(NodeArrayExpression::new(left, token.clone(), false)));
            members.push(Box::new(NodeArrayExpression::new(right, token.clone(), false)));
        }

        if self.eat(Some(TokenType::RBracket)).is_none() {
            return Err(None);
        }

        return Ok(NodeArrayExpression::new(members, token, is_dictionary));
    }

    pub fn parse_object_expression(&mut self) -> Result<NodeObjectExpression, Option<String>> {
        let mut members = Vec::new(); // Array of var declarations

        // Eat left brace
        if self.eat(Some(TokenType::LBrace)).is_none() {
            return Err(None);
        }

        let mut token = self.current_token();

        // Find all lines in block
        while token.token_type != Some(TokenType::RBrace) {
            // Parse variable declaration
            let var_decl = self.parse_variable_declaration(false);

            if var_decl.is_err() {
                self.error("Invalid object member declaration".to_string());
                return Err(var_decl.unwrap_err());
            }

            members.push(var_decl.unwrap());

            token = self.current_token();
        }

        if self.eat(Some(TokenType::RBrace)).is_none() {
            return Err(None);
        }

        return Ok(NodeObjectExpression::new(members));
    }

    pub fn parse_type(&mut self) -> NodeVarType {
        let node = NodeVarType::new(self.current_token());
        self.eat(None);
        return node;
    }

    pub fn parse_function_call(&mut self, node: Box<dyn AstNode>) -> Result<Box<dyn AstNode>, Option<String>> {
        self.eat(Some(TokenType::LParen));
        
        let mut argnames = Vec::new();
        let last = self.current_token();
        
        if self.current_token().token_type != Some(TokenType::RParen) {
            // Skip until RParen
            while self.current_token().token_type != Some(TokenType::RParen) {
                // Append argument to ArgumentList node
                if self.peek_token(0, Some(TokenType::Multiply)).is_some() {
                    // Splat args
                    let vargs_token = self.current_token();
                    self.eat(Some(TokenType::Multiply));
                    let splat_expr = self.parse_expression()?;

                    argnames.push(NodeTokenType::Node(Box::new(NodeSplatArgument::new(splat_expr, vargs_token))));
                }
                else {
                    argnames.push(NodeTokenType::Node(self.parse_expression()?));
                }

                if self.current_token().token_type == Some(TokenType::RParen) {
                    break;
                }

                self.eat(None);

                if self.current_token().token_type == Some(TokenType::NoneToken) {
                    return Ok(Box::new(NodeNone::new(last)));
                }
            }
        }
        
        // Eat closing paren
        self.eat(Some(TokenType::RParen));

        let args = NodeArgumentList::new(argnames, Some(NodeTokenType::Token(self.current_token())));
        
        return Ok(Box::new(NodeCall::new(node, args)));
    }

    pub fn parse_function_expression(&mut self) -> Result<NodeFunctionExpression, Option<String>> {
        if self.eat(Some(TokenType::Keyword)).is_none() {
            return Err(None);
        }

        let argument_list = self.parse_argument_list()?;

        let block = self.parse_block_statement()?;

        return Ok(NodeFunctionExpression::new(argument_list, block));
    }

    pub fn parse_arrow_function(&mut self, node: Box<NodeVariable>) -> Result<NodeFunctionExpression, Option<String>> {
        let token = self.current_token();
    
        let mut arguments = Vec::new();

        match node.token() {
            Some(tok) => match tok {
                NodeTokenType::Token(t) => arguments.push(NodeTokenType::Node(Box::new(NodeDeclare::new(None, t.clone(), Box::new(NodeNone::new(token.clone())), false)))),
                NodeTokenType::Node(_) => unreachable!(),
            },
            None => unreachable!(),
        };

        if self.eat(Some(TokenType::Arrow)).is_none() {
            return Err(None);
        }

        let expr = self.parse_expression()?;

        let return_node = Box::new(NodeFunctionReturn::new(expr, Some(NodeTokenType::Token(token.clone()))));

        let mut block = NodeBlock::new(token.clone());
        block.children = vec![return_node];

        let fun_expr = NodeFunctionExpression::new(
            NodeArgumentList::new(
                arguments,
                Some(NodeTokenType::Token(token))
            ),
            block
        );

        return Ok(fun_expr);
    }

    pub fn parse_func_declaration(&mut self) -> Result<NodeDeclare, Option<String>> {
        // func NAME(...) { ... }
        
        // Eat func keyword
        self.eat(Some(TokenType::Keyword));
        // Eat function name
        let name = self.current_token();
        if self.eat(Some(TokenType::Identifier)).is_none() {
            return Err(None);
        }

        let argument_list = self.parse_argument_list()?;

        let block = self.parse_block_statement()?;

        let fun_expr = NodeFunctionExpression::new(argument_list, block);
        
        // Parse assignment, parenthesis, etc.
        let val_node = NodeAssign::new(Box::new(NodeVariable::new(name.clone(), false)), Box::new(fun_expr));
        let type_node = NodeVariable::new(LexerToken::new("Func".to_string(), Some(TokenType::Identifier)), false);
        let node = NodeDeclare::new(Some(Box::new(type_node)), name, Box::new(val_node), false);
        
        return Ok(node);
    }

    pub fn parse_variable_declaration(&mut self, require_keyword: bool) -> Result<NodeDeclare, Option<String>> {
        // let VARNAME:TYPE parse_assignment_statement
        
        if require_keyword {
            // Eat let keyword
            if self.eat(Some(TokenType::Keyword)).is_none() {
                return Err(None);
            }
        }
        else {
            match self.peek_token(0, Some(TokenType::Keyword)) {
                Some(t) => {
                    if t.value == "func".to_string() {
                        return self.parse_func_declaration();
                    }
                },
                None => {}
            }
        }
            
        let name = self.current_token();
        if self.eat(Some(TokenType::Identifier)).is_none() {
            return Err(None);
        }

        let mut type_node = None;
        let mut allow_casting = false;
        
        // Manual type set
        if self.current_token().token_type == Some(TokenType::Colon) {
            self.eat(Some(TokenType::Colon));
            let type_node_token = self.current_token();
            type_node = Some(self.parse_factor()?);

            if type_node.is_none() || (type_node.as_ref().unwrap().node_type() != NodeType::Variable && type_node.as_ref().unwrap().node_type() != NodeType::MemberExpression) {
                self.error(format!("Declaration type should either be an identifier or member access, got {:?}", type_node_token));
                return Err(None);
            }

            if self.current_token().token_type == Some(TokenType::Question) {
                self.eat(Some(TokenType::Question));
                allow_casting = true;
            }
        }

        let val_node: Box<dyn AstNode>;
        if self.current_token().token_type == Some(TokenType::Equals) {
            val_node = Box::new(self.parse_assignment_statement(Box::new(NodeVariable::new(name.clone(), allow_casting)), true)?);
        }
        else {
            val_node = Box::new(NodeNone::new(name.clone()));
        }

        let vnodes = NodeDeclare::new(type_node, name, val_node, allow_casting);
        
        return Ok(vnodes);
    }

    pub fn parse_if_statement(&mut self) -> Result<NodeIfStatement, Option<String>> {
        // Eat `if`
        let if_token = self.current_token();
        if self.eat(Some(TokenType::Keyword)).is_none() {
            return Err(None);
        }

        let expr = self.parse_expression()?;

        let block = self.parse_block_statement()?;

        let mut else_block: Option<Box<dyn AstNode>> = None;
        
        let token = self.current_token();

        if token.token_type == Some(TokenType::Keyword) {
            if Keywords::from_str(token.value.as_str()) == Ok(Keywords::Else) {
                // Eat else
                self.eat(Some(TokenType::Keyword));
                else_block = Some(Box::new(self.parse_block_statement()?));
            }
            else if Keywords::from_str(token.value.as_str()) == Ok(Keywords::Elif) {
                else_block = Some(Box::new(self.parse_if_statement()?));
            }
        }
        
        return Ok(NodeIfStatement::new(expr, block, else_block, if_token));
    }

    pub fn parse_try(&mut self) -> Result<NodeTryCatch, Option<String>> {
        // Eat `try`
        let try_token = self.current_token();
        if self.eat(Some(TokenType::Keyword)).is_none() {
            return Err(None);
        }

        let block = self.parse_block_statement()?;

        let mut catch_block = Vec::new();
        
        let mut token = self.current_token();
        let mut expr: Vec<NodeOrVec> = Vec::new();
        let mut variable = Vec::new();

        let mut else_block: Option<Box<dyn AstNode>> = None;
        let mut finally_block: Option<Box<dyn AstNode>> = None;

        while token.token_type == Some(TokenType::Keyword) && Keywords::from_str(token.value.as_str()) == Ok(Keywords::Catch) {
            // Eat catch
            self.eat(Some(TokenType::Keyword));

            if self.current_token().token_type == Some(TokenType::LBracket) {
                let mut values: Vec<Box<dyn AstNode>> = Vec::new();
                while self.current_token().token_type != Some(TokenType::RBracket) {
                    if self.current_token().token_type != Some(TokenType::Comma) && self.current_token().token_type != Some(TokenType::LBracket) {
                        values.push(Box::new(NodeString::new(self.current_token())));
                    }
                    self.eat(self.current_token().token_type);
                }
                self.eat(self.current_token().token_type);
                expr.push(NodeOrVec::Vec(values));

                if self.current_token().token_type == Some(TokenType::Identifier) {
                    let e = self.parse_expression()?;
                    println!("{:?}", e);
                }
            }
            else if self.current_token().token_type == Some(TokenType::LBrace) {
                expr.push(NodeOrVec::Node(Box::new(NodeString::new(LexerToken::new("Exception".to_string(), None)))));
            }
            else if self.current_token().token_type == Some(TokenType::Identifier) {
                expr.push(NodeOrVec::Node(self.parse_expression()?));
    
                if self.current_token().token_type == Some(TokenType::Identifier) {
                    let e = self.parse_expression()?;
                    let val_node = NodeAssign::new(Box::new(NodeVariable::new(match e.token() {
                        Some(t) => match t {
                            NodeTokenType::Token(tok) => tok,
                            NodeTokenType::Node(_) => unreachable!(),
                        },
                        None => unreachable!(),
                    }, false)), match expr.last().unwrap() {
                        NodeOrVec::Node(val) => val.clone(),
                        NodeOrVec::Vec(_) => unreachable!(),
                    });
                    let type_node = NodeVariable::new(LexerToken::new("Exception".to_string(), Some(TokenType::Identifier)), false);
                    // let type_node_token = self.current_token();
                    // type_node = self.parse_factor();
                    let n = NodeDeclare::new(Some(Box::new(type_node)), match e.token() {
                        Some(t) => match t {
                            NodeTokenType::Token(tok) => tok,
                            NodeTokenType::Node(_) => unreachable!(),
                        },
                        None => unreachable!(),
                    }, Box::new(val_node), false);
                    variable.push(Some(n));
                }
                else if self.current_token().token_type == Some(TokenType::LBrace) {
                    variable.push(None);
                }
            }

            catch_block.push(self.parse_block_statement()?);
            token = self.current_token();
        }
        if token.token_type == Some(TokenType::Keyword) && Keywords::from_str(token.value.as_str()) == Ok(Keywords::Else) {
            // Eat else
            self.eat(Some(TokenType::Keyword));

            else_block = Some(Box::new(self.parse_block_statement()?));
            
            token = self.current_token();
        }
        if token.token_type == Some(TokenType::Keyword) && Keywords::from_str(token.value.as_str()) == Ok(Keywords::Finally) {
            // Eat finally
            self.eat(Some(TokenType::Keyword));

            finally_block = Some(Box::new(self.parse_block_statement()?));
            
            // token = self.current_token();
        }
        
        return Ok(NodeTryCatch::new(block, catch_block, expr, else_block, finally_block, try_token, variable));
    }

    pub fn parse_factor(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        // Handles value or (x ± x)
        let token = self.current_token();

        let mut node: Option<Box<dyn AstNode>> = None;

        // Handle +, -
        if token.token_type == Some(TokenType::Plus) || token.token_type == Some(TokenType::Minus) {
            self.eat(token.clone().token_type);
            node = Some(Box::new(NodeUnaryOp::new(token, self.parse_factor()?)));
        }
        
        // Handle '!'
        else if token.token_type == Some(TokenType::Not) {
            self.eat(Some(TokenType::Not));
            node = Some(Box::new(NodeUnaryOp::new(token, self.parse_factor()?)));
        }

        // Handle '~'
        else if token.token_type == Some(TokenType::BitwiseNot) {
            self.eat(Some(TokenType::BitwiseNot));
            node = Some(Box::new(NodeUnaryOp::new(token, self.parse_factor()?)));
        }
            
        else if token.token_type == Some(TokenType::Number) {
            self.eat(Some(TokenType::Number));
            node = Some(Box::new(NodeNumber::new(token)));
        }
        
        else if token.token_type == Some(TokenType::String) {
            self.eat(Some(TokenType::String));
            node = Some(Box::new(NodeString::new(token)));
        }
        
        else if token.token_type == Some(TokenType::LParen) {
            self.eat(Some(TokenType::LParen));
            node = Some(self.parse_expression()?);
            self.eat(Some(TokenType::RParen));
        }
        else if token.token_type == Some(TokenType::LBracket) {
            node = Some(Box::new(self.parse_array_expression()?));
        }
        else if token.token_type == Some(TokenType::LBrace) {
            node = Some(Box::new(self.parse_object_expression()?));
        }
        else if token.token_type == Some(TokenType::Identifier) {
            let variable_node = Box::new(self.parse_variable());
            node = Some(variable_node.clone());

            if self.peek_token(0, Some(TokenType::Arrow)).is_some() {
                node = Some(Box::new(self.parse_arrow_function(variable_node)?));
            }
        }
        else if token.token_type == Some(TokenType::Keyword) {
            if Keywords::from_str(token.value.as_str()) == Ok(Keywords::Func) {
                node = Some(Box::new(self.parse_function_expression()?));
            }
            else {
                self.error(format!("Invalid usage of keyword {} in expression", token.value));
                return Err(None);
            }
        }

        if node.is_none() {
            self.error(format!("Unexpected token: {}", self.current_token()));
            self.eat(None);
            return Err(None);
        }

        while self.current_token().token_type == Some(TokenType::Dot) || self.current_token().token_type == Some(TokenType::LParen) || self.current_token().token_type == Some(TokenType::LBracket) {
            if self.peek_token(0, Some(TokenType::Dot)).is_some() {
                node = Some(Box::new(self.parse_member_expression(node.unwrap())?));
            }
            else if self.peek_token(0, Some(TokenType::LBracket)).is_some() {
                node = Some(Box::new(self.parse_array_access_expression(node.unwrap())?));
            }
            else if self.peek_token(0, Some(TokenType::LParen)).is_some() {
                node = Some(self.parse_function_call(node.unwrap())?);
            }
        }

        if node.is_none() {
            return Err(None);
        }

        return Ok(node.unwrap());
    }

    pub fn parse_term(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        // Handles multiply, division, expressions
        let mut node = self.parse_factor()?;
        while self.current_token().token_type == Some(TokenType::Multiply) || self.current_token().token_type == Some(TokenType::Divide) {
            let token = self.current_token();
            if token.token_type == Some(TokenType::Multiply) {
                self.eat(Some(TokenType::Multiply));
            }
            else if token.token_type == Some(TokenType::Divide) {
                self.eat(Some(TokenType::Divide));
            }
            node = Box::new(NodeBinOp::new(node, token, self.parse_factor()?));
        }
        return Ok(node);
    }

    pub fn parse_expression(&mut self) -> Result<Box<dyn AstNode>, Option<String>> {
        let mut node = self.parse_term()?;
        
        let mut multiop_types = vec![
            TokenType::PlusEquals, TokenType::MinusEquals, 
            TokenType::MultiplyEquals, TokenType::DivideEquals,
            TokenType::ModulusEquals,
            TokenType::BitwiseOrEquals, TokenType::BitwiseAndEquals,
            TokenType::BitwiseXorEquals,
            TokenType::BitwiseLShiftEquals, TokenType::BitwiseRShiftEquals
        ];
        
        let mut expected_types = vec![
            TokenType::Equals,
            TokenType::Plus, TokenType::Minus, TokenType::Modulus,
            TokenType::Compare, TokenType::NotCompare,
            TokenType::Spaceship,
            TokenType::Arrow,
            TokenType::LessThan, TokenType::GreaterThan,
            TokenType::LessThanEqual, TokenType::GreaterThanEqual,
            TokenType::BitwiseOr, TokenType::BitwiseAnd, TokenType::BitwiseXor,
            TokenType::And, TokenType::Or,
            TokenType::BitwiseLShift, TokenType::BitwiseRShift,
            TokenType::Exponentiation
        ];
        expected_types.append(&mut multiop_types);

        while self.current_token().token_type.is_some() && expected_types.contains(&self.current_token().token_type.unwrap()) {
            let token = self.current_token();
        
            if self.peek_token(0, Some(TokenType::Equals)).is_some() {
                node = Box::new(self.parse_assignment_statement(node, true)?);
                continue;
            }
                
            if self.current_token().token_type.is_some() && multiop_types.contains(&self.current_token().token_type.unwrap()) {
                // Parse (lhs [operator] rhs) and return assign node
                let mut assign_node = Box::new(self.parse_assignment_statement(node.clone(), true)?);
                
                // This is slightly sketchy, but also will be able to handle
                // operations like <<= and any other multichar operation
                let operation = LexerToken::new(token.value.trim_matches('=').to_string(), None);
                
                // Make value (lhs [operator] rhs)
                let value_node = Box::new(NodeBinOp::new(node, operation, assign_node.value));
                
                // Final node should be (lhs [=] lhs [operator] rhs)
                assign_node.value = value_node;
                node = assign_node;
                continue;
            }

            if token.token_type.is_some() && expected_types.contains(&token.token_type.clone().unwrap()) {
                self.eat(None);
            }
                
            if (token.token_type == Some(TokenType::Or) || token.token_type == Some(TokenType::And)) && self.peek_token(1, None).unwrap().token_type.is_some() && expected_types.contains(&self.peek_token(1, None).unwrap().token_type.unwrap()) {
                node = Box::new(NodeBinOp::new(node, token, self.parse_expression()?));
                continue;
            }
                
            node = Box::new(NodeBinOp::new(node, token, self.parse_term()?));
        }
        return Ok(node);
    }

    pub fn parse(&mut self) -> Result<Vec<Box<dyn AstNode>>, Option<String>> {
        return self.get_statements();
    }
}
