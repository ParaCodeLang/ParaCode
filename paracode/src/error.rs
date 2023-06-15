use std::fmt;

use crate::interpreter::basic_wrapper::BasicWrapper;
use crate::parse::node::AstNode;
use crate::utils::LogColor;

pub struct InterpreterError<'a> {
    node: Box<dyn AstNode>,
    ty: ErrorType,
    message: String,
    cont: bool,
    name: String,
    classnames: Vec<String>,
    object: Option<&'a BasicWrapper<'a>>,
}
impl<'a> InterpreterError<'a> {
    pub fn new(
        node: Box<dyn AstNode>,
        ty: ErrorType,
        message: String,
        cont: bool,
        name: String,
        classnames: Vec<String>,
        object: Option<&'a BasicWrapper<'a>>,
    ) -> InterpreterError<'a> {
        return InterpreterError {
            node: node,
            ty: ty,
            message: message,
            cont: cont,
            name: name,
            classnames: classnames,
            object: object,
        };
    }
}
impl<'a> fmt::Display for InterpreterError<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "Interpreter error");
    }
}

#[derive(Eq, PartialEq, Clone, Debug, EnumString, strum_macros::Display, AsRefStr)]
pub enum ErrorType {
    #[strum(serialize = "Exception", serialize = "1")]
    Exception,
    #[strum(serialize = "Syntax", serialize = "2")]
    Syntax,
    #[strum(serialize = "DoesNotExist", serialize = "3")]
    DoesNotExist,
    #[strum(serialize = "TypeError", serialize = "4")]
    TypeError,
    #[strum(serialize = "MultipleDefinition", serialize = "5")]
    MultipleDefinition,
    #[strum(serialize = "ArgumentError", serialize = "6")]
    ArgumentError,
    #[strum(serialize = "MacroExpansionError", serialize = "7")]
    MacroExpansionError,
    #[strum(serialize = "InterruptedError", serialize = "8")]
    InterruptedError,
}

#[derive(Eq, PartialEq, Clone)]
pub struct Error {
    ty: ErrorType,
    filename: String,
    message: String,
    location: (i32, i32),
    name: String,
}
impl Error {
    pub fn new(
        ty: ErrorType,
        location: (i32, i32),
        message: String,
        filename: String,
        name: String,
    ) -> Error {
        return Error {
            ty: ty,
            filename: filename,
            message: message,
            location: location,
            name: name,
        };
    }

    pub fn location_filename(&self) -> String {
        if self.filename.as_str() == "" {
            return "<none>".to_string();
        }

        return self.filename.clone();
    }

    pub fn location_row(&self) -> i32 {
        return self.location.1;
    }

    pub fn location_col(&self) -> i32 {
        return self.location.0;
    }
}
impl<'a> fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let nstr = format!(
            "{}:{}:{}: {}{}:{}",
            self.location_filename(),
            self.location_row(),
            self.location_col(),
            LogColor::error(),
            self.name,
            LogColor::default()
        );
        // let mut nstr = format!("{}:{}:{}: {}{} error:{}", self.location_filename(), self.location_row(), self.location_col(), LogColor::error($, self.type.name, LogColor::default());
        // if self.type == ErrorType::Exception {
        //     nstr = format!("{}:{}:{}: {}{}:{}", self.location_filename(), self.location_row(), self.location_col(), LogColor::error(), self.name, LogColor::default());
        // }
        return write!(
            f,
            "{}{}{} {}",
            LogColor::bold(),
            nstr,
            LogColor::default(),
            self.message
        );
    }
}
impl<'a> fmt::Debug for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", self);
    }
}

pub struct ErrorList {
    pub errors: Vec<Error>,
}
impl ErrorList {
    pub fn new() -> ErrorList {
        return ErrorList { errors: Vec::new() };
    }

    pub fn clear_errors(&mut self) {
        self.errors.clear();
    }

    pub fn push_error(&mut self, error: Error) {
        self.errors.push(error);
    }

    pub fn print_errors(&self) {
        for error in self.errors.iter() {
            println!("{}", error);
        }
    }

    pub fn get_errors(&self) -> &Vec<Error> {
        return &self.errors;
    }
}
