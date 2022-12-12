use std::collections::HashMap;

use crate::lexer::LexerToken;
use crate::parse::node::AstNode;
use crate::parse::source_location::SourceLocation;
use crate::error::ErrorList;

pub struct Parser<'a> {
    tokens: Vec<Box<LexerToken>>,
    token_index: i32,
    current_token: Box<LexerToken>,
    error_list: ErrorList,

    source_location: SourceLocation,

    keyword_methods: HashMap<&'a String, fn(Self) -> &'a dyn AstNode<'a>>,
}
impl<'a> Parser<'a> {
    pub fn new(tokens: Vec<Box<LexerToken>>, source_location: SourceLocation) -> Parser<'a> {
        let mut parser = Parser {
            tokens: tokens,
            token_index: 0,
            current_token: Box::new(LexerToken::none()),
            error_list: ErrorList::new(),

            source_location: source_location,

            keyword_methods: HashMap::from([
                // ("let".to_string(), self.parse_variable_declaration),
                // ("if".to_string(), self.parse_if_statement),
                // ("func".to_string(), self.parse_func_declaration),
                // ("import".to_string(), self.parse_import),
                // ("return".to_string(), self.parse_return),
                // ("while".to_string(), self.parse_while),
                // ("for".to_string(), self.parse_for),
                // ("macro".to_string(), self.parse_macro),
                // ("mixin".to_string(), self.parse_mixin),
                // ("try".to_string(), self.parse_try),
            ])
        };
        parser.current_token = parser.next_token();
        return parser;
    }

    pub fn filename(&self) -> &String {
        return &self.source_location.filename;
    }

    /*
    pub fn expect_token(self, token_type, offset=0, token=None) {
        // If no token passed in, peek from offset
        if token == None {
            token = self.peek_token(offset);
        }

        if token.type == token_type {
            return token;
        }
        else {
            self.error('expected {0} but recieved {1}'.format(token_type.name, token.type.name));
            return None;
        }
    }
    */

    pub fn next_token(&mut self) -> Box<LexerToken> {
        // Check if next index is past list boundaries
        if (self.token_index + 1) as usize > self.tokens.len() {
            return Box::new(LexerToken::none());
        }
        
        // Return selected token, increment index
        self.current_token = self.tokens[self.token_index as usize].clone();
        self.token_index += 1;
        
        return self.current_token.clone();
    }

    // Return token at token.index + offset
    /*pub fn peek_token(&self, offset: i32, expected_type: TokenType) -> Box<LexerToken> {
        // Check bounds
        if self.token_index+offset-1 > len(self.tokens):
            return None;
        }
            
        token = self.tokens[self.token_index+offset-1]
        
        // Check type if expected_type != None
        if expected_type != None and token.type != expected_type:
            return None;
        }
        
        return token;
    }*/

    // error

    // eat

    // parse_variable

    // parse_member_expression

    // parse_array_access_expression

    // import_file

    // parse_while

    // parse_for

    // parse_macro

    // parse_mixin

    // parse_import

    // parse_return

    // parse_assignment_statement

    // parse_argument_list

    // parse_parenthesis

    // parse_statement

    // get_statements

    // parse_keyword

    // parse_block_statement

    // parse_array_expression

    // parse_object_expression

    // parse_type

    // parse_function_call

    // parse_function_expression

    // parse_arrow_function

    // parse_func_declaration

    // parse_variable_declaration

    // parse_if_statement

    // parse_try

    // parse_factor

    // parse_term

    // parse_expression

    // parse
}
