use std::fmt;
use std::str::FromStr;
use std::collections::HashMap;

use crate::parse::source_location::SourceLocation;

#[derive(Eq, PartialEq, Debug, EnumString, strum_macros::Display)]
pub enum Keywords {
    #[strum(serialize="let")]
    Let,
    #[strum(serialize="if")]
    If,
    #[strum(serialize="else")]
    Else,
    #[strum(serialize="elif")]
    Elif,
    #[strum(serialize="func")]
    Func,
    #[strum(serialize="import")]
    Import,
    #[strum(serialize="return")]
    Return,
    #[strum(serialize="while")]
    While,
    #[strum(serialize="for")]
    For,
    #[strum(serialize="in")]
    In,
    #[strum(serialize="macro")]
    Macro,
    #[strum(serialize="mixin")]
    Mixin,
    #[strum(serialize="try")]
    Try,
    #[strum(serialize="catch")]
    Catch,
    #[strum(serialize="finally")]
    Finally
}

#[derive(Eq, PartialEq, Debug, EnumString, strum_macros::Display)]
pub enum TokenType {
    #[strum(serialize="1", serialize="NoneToken")]
    NoneToken,

    #[strum(serialize="(", serialize="LParen")]
    LParen,
    #[strum(serialize=")", serialize="RParen")]
    RParen,
    #[strum(serialize="{", serialize="LBrace")]
    LBrace,
    #[strum(serialize="}", serialize="RBrace")]
    RBrace,
    #[strum(serialize="[", serialize="LBracket")]
    LBracket,
    #[strum(serialize="]", serialize="RBracket")]
    RBracket,
    #[strum(serialize="+", serialize="Plus")]
    Plus,
    #[strum(serialize="-", serialize="Minus")]
    Minus,
    #[strum(serialize="*", serialize="Multiply")]
    Multiply,
    #[strum(serialize="**", serialize="Exponentiation")]
    Exponentiation,
    #[strum(serialize="/", serialize="Divide")]
    Divide,
    #[strum(serialize="=", serialize="Equals")]
    Equals,
    #[strum(serialize=";", serialize="Semicolon")]
    Semicolon,
    #[strum(serialize=":", serialize="Colon")]
    Colon,
    #[strum(serialize=".", serialize="Dot")]
    Dot,
    #[strum(serialize=",", serialize="Comma")]
    Comma,
    #[strum(serialize="!", serialize="Not")]
    Not,
    #[strum(serialize="?", serialize="Question")]
    Question,
    #[strum(serialize="%", serialize="Modulus")]
    Modulus,
    #[strum(serialize="<", serialize="LessThan")]
    LessThan,
    #[strum(serialize="<=", serialize="LessThanEqual")]
    LessThanEqual,
    #[strum(serialize=">", serialize="GreaterThan")]
    GreaterThan,
    #[strum(serialize=">=", serialize="GreaterThanEqual")]
    GreaterThanEqual,

    #[strum(serialize="&&", serialize="And")]
    And,
    #[strum(serialize="||", serialize="Or")]
    Or,
    
    #[strum(serialize="|", serialize="BitwiseOr")]
    BitwiseOr,
    #[strum(serialize="&", serialize="BitwiseAnd")]
    BitwiseAnd,
    #[strum(serialize="^", serialize="BitwiseXor")]
    BitwiseXor,
    #[strum(serialize="~", serialize="BitwiseNot")]
    BitwiseNot,
    #[strum(serialize="<<", serialize="BitwiseLShift")]
    BitwiseLShift,
    #[strum(serialize=">>", serialize="BitwiseRShift")]
    BitwiseRShift,
    
    #[strum(serialize="==", serialize="Compare")]
    Compare,
    #[strum(serialize="!=", serialize="NotCompare")]
    NotCompare,
    #[strum(serialize="<=>", serialize="Spaceship")]
    Spaceship,

    #[strum(serialize="->", serialize="Arrow")]
    Arrow,
    
    #[strum(serialize="+=", serialize="PlusEquals")]
    PlusEquals,
    #[strum(serialize="-=", serialize="MinusEquals")]
    MinusEquals,
    #[strum(serialize="*=", serialize="MultiplyEquals")]
    MultiplyEquals,
    #[strum(serialize="/=", serialize="DivideEquals")]
    DivideEquals,
    #[strum(serialize="%=", serialize="ModulusEquals")]
    ModulusEquals,
    #[strum(serialize="|=", serialize="BitwiseOrEquals")]
    BitwiseOrEquals,
    #[strum(serialize="&=", serialize="BitwiseAndEquals")]
    BitwiseAndEquals,
    #[strum(serialize="^=", serialize="BitwiseXorEquals")]
    BitwiseXorEquals,
    #[strum(serialize="<<=", serialize="BitwiseLShiftEquals")]
    BitwiseLShiftEquals,
    #[strum(serialize=">>=", serialize="BitwiseRShiftEquals")]
    BitwiseRShiftEquals,

    #[strum(serialize="2", serialize="Identifier")]
    Identifier,
    #[strum(serialize="3", serialize="Number")]
    Number,
    #[strum(serialize="4", serialize="String")]
    String,
    #[strum(serialize="5", serialize="Keyword")]
    Keyword
}
impl TokenType {
    pub fn get_type(value: &String) -> Option<TokenType> {
        if value.is_empty() {
            return None;
        }
            
        if !TokenType::from_str(value.as_str()).is_err() {
            return Some(TokenType::from_str(value.as_str()).unwrap());
        }

        if value.chars().nth(0).unwrap().is_numeric() || value.chars().nth(0).unwrap() == '.' {
            // What?
            if value.len() > 1 {
                if value.chars().nth(1).unwrap() == 'x' || value.chars().nth(1).unwrap() == 'X' {
                    return Some(TokenType::Number);
                }
            }
                    
            if value.contains(".") {
                return Some(TokenType::Number);
            }
            return Some(TokenType::Number);
        }
        
        else if (value.chars().nth(0).unwrap() == '"' && value.chars().last().unwrap() == '"') || (value.chars().nth(0).unwrap() == '\'' && value.chars().last().unwrap() == '\'') {
            return Some(TokenType::String);
        }
        
        // Check if string is keyword
        if !Keywords::from_str(value.as_str()).is_err() {
            return Some(TokenType::Keyword);
        }
        
        // Nothing else, must be identifier
        return Some(TokenType::Identifier);
    }

    pub fn has_value(value: String) -> bool {
        return !TokenType::from_str(value.as_str()).is_err();
    }
}

#[derive(Debug)]
pub struct LexerToken {
    pub token_type: Option<TokenType>,
    pub value: String,
    pub location: (i32, i32),
}
impl LexerToken {
    const EMPTY_STRING: String = String::new();
    
    pub fn none() -> LexerToken {
        return LexerToken::new(LexerToken::EMPTY_STRING, Some(TokenType::NoneToken));
    }
    
    pub fn new(value: String, token_type: Option<TokenType>) -> LexerToken {
        return LexerToken {
            token_type: match token_type {
                Some(t) => Some(t),
                None => TokenType::get_type(&value),
            },
            value: value,
            location: (0, 0),
        };
    }
}
impl fmt::Display for LexerToken {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "LexerToken[Type:{}, Value:'{}']", match &self.token_type {
            Some(t) => format!("{}", t),
            None => "None".to_string(),
        }, self.value);
    }
}
impl PartialEq<LexerToken> for LexerToken {
    fn eq(&self, _rhs: &LexerToken) -> bool {
        return self.token_type == _rhs.token_type && self.value == _rhs.value && self.location == _rhs.location;
    }

    fn ne(&self, _rhs: &LexerToken) -> bool {
        return !(self == _rhs);
    }
}

pub struct Lexer<'a> {
    pub tokens: Vec<LexerToken>,
    pub data: &'a String,
    pub token_data: String,
    pub index: i32,
    pub source_location: SourceLocation
}
impl<'a> Lexer<'a> {
    pub fn new(data: &'a String, source_location: SourceLocation) -> Lexer<'a> {
        let mut result = Lexer {
            tokens: Vec::new(),
            data: data,
            token_data: "".to_string(),
            index: 0,
            source_location: source_location
        };

        // Error handling
        result.source_location.row = 0;
        result.source_location.col = 0;
        
        return result;
    }

    // Return character and progress through buffer
    pub fn read_char(&mut self, amt: i32) -> String {
        if ((self.index + amt) as usize) > self.data.len() {
            return "".to_string();
        }
        let rval = self.data.chars().take((self.index + 1) as usize).skip(self.index as usize).collect();
        self.index += amt;
        self.source_location.col += 1;
        if rval == "\n" {
            self.source_location.col += 1;
            self.source_location.row += 1;
        }
        return rval;
    }

    // Return character and keep index
    pub fn peek_char(&self, offset: i32) -> String {
        let idx = self.index + offset;
        if (idx as usize) >= self.data.len() || idx < 0 {
            return "".to_string();
        }
        return self.data.chars().nth(idx as usize).unwrap().to_string();
    }

    pub fn push_token(&mut self) -> Result<(), String> {
        let mut token = LexerToken::new(self.token_data.clone(), None);
        if self.token_data.is_empty() {
            return Err("tokendata blank".to_string());
        }
        token.location = self.source_location.col_row();
        self.tokens.push(token);
        self.token_data.clear();
        
        return Ok(());
    }

    pub fn skip_whitespace(&mut self) -> bool {
        if self.peek_char(0).len() > 0 && self.peek_char(0).chars().all(|c| c.is_whitespace()) {
            while self.peek_char(0).len() > 0 && self.peek_char(0).chars().all(|c| c.is_whitespace()) {
                self.read_char(1);
            }
            return true;
        }
        return false;
    }

    pub fn lex(&mut self) -> Result<&Vec<LexerToken>, String> {
        let splitables = "(){}[];:+-*/=.,!?|&~<>^%".to_string();
        let multichar_splitables = vec![
            "**", "<=>", "<<=", ">>=",
            "|=", "&=", "^=",
            "==", "!=", "<=", ">=",
            "+=", "-=", "*=", "/=",
            "%=", "==", "!=", "->",
            "&&", "||", "<<", ">>"
        ];

        let escape_chars = HashMap::from([
            ("n", "\n"),
            ("b", "\x08"),
            ("t", "\t"),
            ("v", "\x0b"),
            ("a", "\x07"),
            ("r", "\r"),
            ("f", "\x0c"),
            ("033", "\x1b"),
            ("x1b", "\x1b"),
            ("\\", "\\"),
            ("'", "\'"),
            ("\"", "\"")
        ]);

        self.skip_whitespace();

        let mut string_type = "";

        while self.peek_char(0) != "" {
            if string_type != "" && self.peek_char(0) == "\\" {
                // Skip '/'
                self.read_char(1);
                let escape_char = self.read_char(1);
                if escape_chars.contains_key(escape_char.as_str()) {
                    self.token_data += escape_chars[escape_char.as_str()];
                }
                else {
                    println!("Error: Unknown escape character '{}'", escape_char);
                }
                continue;
            }

            // Comments
            if string_type == "" && (self.peek_char(0) == "#" || (self.peek_char(0) == "/" && self.peek_char(1) == "/") || (self.peek_char(0) == "/" || self.peek_char(1) == "*")) {
                let comment_char = self.read_char(1);
                if comment_char == "#" && self.peek_char(0) == "*" {
                    // Multiline comment
                    
                    // Skip '*' character
                    self.read_char(1);

                    // Read until '*#'
                    while self.read_char(1) != "*" && self.peek_char(1) != "#" {
                        // EOF
                        if self.peek_char(0) == "" {
                            break;
                        }
                    }
                                            
                    // Skip '*#' characters
                    self.read_char(2);
                    
                    // End by pushing the token and skipping any whitespace afterwards
                    if self.token_data != "" {
                        self.push_token()?;
                    }
                    self.skip_whitespace();
                }
                else if comment_char == "/" && self.peek_char(0) == "*" {
                    // Multiline comment
                    
                    // Skip '*' character
                    self.read_char(1);

                    // Read until '*/'
                    while self.read_char(1) != "*" && self.peek_char(1) != "/" {
                        // EOF
                        if self.peek_char(0) == "" {
                            break;
                        }
                    }
                        
                    // Skip '*/' characters
                    self.read_char(2);
                    
                    // End by pushing the token and skipping any whitespace afterwards
                    if self.token_data != "" {
                        self.push_token()?;
                    }
                    self.skip_whitespace();
                }
                else {
                    while self.read_char(1) != "\n" {
                        // EOF
                        if self.peek_char(0) == "" {
                            break;
                        }
                    }
                    // Skip any whitespace after comment
                    self.skip_whitespace();
                }
                continue;
            }

            // Encountered whitespace and not in string, push token
            else if string_type == "" && self.skip_whitespace() {
                self.push_token()?;
                continue;
            }

            else if splitables.contains(self.peek_char(0).as_str()) && string_type == "" {
                if !(self.peek_char(-1).len() > 0 && self.peek_char(-1).chars().all(|c| c.is_whitespace())) && !splitables.contains(self.peek_char(-1).as_str()) && self.token_data.len() > 0 {
                    self.push_token()?;
                }

                let mut multichar = false;

                for tok in &multichar_splitables {
                    let idx = &self.data.chars().take(self.index as usize).skip((self.index as usize) + tok.len()).collect::<String>().find(tok);
                    if idx.is_some() {
                        for _ in 0..tok.chars().count() {
                            let char = &self.read_char(1);
                            self.token_data += char;
                        }

                        multichar = true;
                    }
                }
                
                // if (self.peek_char(-1).chars().count() > 0 && self.peek_char(-1).chars().all(|c| c.is_numeric())) && self.peek_char(0) == "." {
                //     let char = &self.read_char(1);
                //     self.token_data += char;
                //     continue;
                // }
                
                if !multichar {
                    self.token_data = self.read_char(1);
                }

                self.push_token()?;
                self.skip_whitespace();
                continue;
            }
            else if (self.peek_char(0).len() > 0 && self.peek_char(0).chars().all(|c| c.is_numeric())) && string_type == "" {
                let mut is_float = false;

                while self.peek_char(0).len() > 0 && self.peek_char(0).chars().all(|c| c.is_numeric()) {
                    let char = &self.read_char(1);
                    self.token_data += char;

                    if !is_float && self.peek_char(0) == "." {
                        // If next char is identifier, its not float,
                        // rather it could be something like
                        // `1.to_str()`
                        if !(self.peek_char(1).len() > 0 && self.peek_char(1).chars().all(|c| c.is_numeric())) {
                            break;
                        }

                        let char = &self.read_char(1);
                        self.token_data += char;
                        is_float = true;
                    }
                }

                self.push_token()?;
                self.skip_whitespace();
                continue;
            }

            // Check if string character
            if self.peek_char(0) == "\"" {
                // If currently in double quotes string, end and set string_type to none
                if string_type == "\"" {
                    string_type = "";
                }
                // If no string is open, open a new one
                else if string_type == "" {
                    string_type = "\"";
                }
                // If currently in single quotes string, ignore
            }

            else if self.peek_char(0) == "'" {
                if string_type == "'" {
                    string_type = "";
                }
                else if string_type == "" {
                    string_type = "'";
                }
            }

            
            let char = &self.read_char(1);
            self.token_data += char;
        }
        // Still some data left in token_data, push to end
        if self.token_data != "" {
            self.push_token()?;
        }

        return Ok(&self.tokens);
    }
}
