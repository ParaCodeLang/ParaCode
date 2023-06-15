pub mod error;
pub mod interpreter;
pub mod lexer;
pub mod paracode;
pub mod parse;
pub mod extensions;
pub mod utils;

extern crate strum;
#[macro_use]
extern crate strum_macros;

#[macro_use]
extern crate downcast_rs;

#[macro_use]
extern crate lazy_static;
