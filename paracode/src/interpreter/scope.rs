use std::collections::HashMap;

use crate::interpreter::basic_wrapper::BasicWrapper;
use crate::interpreter::basic_value::Null;

pub struct SymbolInfo<'a> {
    pub varname: &'a String,
    pub decltype: Box<BasicWrapper>, // Should only be a type
    pub value_wrapper: Box<BasicWrapper>,
    pub allow_casting: bool,
}
impl<'a> SymbolInfo<'a> {
    pub fn new(varname: &String, decltype: Box<BasicWrapper>, value: Box<BasicWrapper>, allow_casting: bool) -> SymbolInfo {
        return SymbolInfo {
            varname: varname,
            decltype: decltype,
            value_wrapper: value,
            allow_casting: allow_casting,
        };
    }
}

pub struct Scope<'a> {
    pub variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>,
    pub parent: Box<Scope<'a>>,
}
impl<'a> Scope<'a> {
    pub fn new(variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>, parent: Box<Scope<'a>>) -> Scope<'a> {
        return Scope {
            variables: variables,
            parent: parent,
        };
    }

    pub fn declare_variable(&mut self, name: &'a String, decltype: Box<BasicWrapper>, allow_casting: bool) -> &Box<BasicWrapper> {
        self.variables.insert(name, SymbolInfo::new(name, decltype, Box::new(BasicWrapper::from_value(Box::new(Null{}))), allow_casting));

        return &self.variables[name].value_wrapper;
    }

    // set_variable

    // find_variable_info

    // find_variable_value

    // find_variable_decltype

    // to_string
}
