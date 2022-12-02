pub mod error;
pub mod lexer;
pub mod parse;
pub mod interpreter;
pub mod paracode;
pub mod utils;

extern crate strum;
#[macro_use]
extern crate strum_macros;

#[macro_use]
extern crate downcast_rs;
