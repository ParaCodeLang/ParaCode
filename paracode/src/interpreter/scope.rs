use std::collections::HashMap;

use crate::interpreter::basic_value::Null;
use crate::interpreter::basic_wrapper::BasicWrapper;

#[derive(Debug)]
pub struct SymbolInfo<'a> {
    pub varname: &'a String,
    pub decltype: Box<BasicWrapper<'a>>, // Should only be a type
    pub value_wrapper: Box<BasicWrapper<'a>>,
    pub allow_casting: bool,
}
impl<'a> SymbolInfo<'a> {
    pub fn new(
        varname: &'a String,
        decltype: Box<BasicWrapper<'a>>,
        value: Box<BasicWrapper<'a>>,
        allow_casting: bool,
    ) -> SymbolInfo<'a> {
        return SymbolInfo {
            varname: varname,
            decltype: decltype,
            value_wrapper: value,
            allow_casting: allow_casting,
        };
    }
}

#[derive(Debug)]
pub struct Scope<'a> {
    pub variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>,
    pub parent: Box<Scope<'a>>,
}
impl<'a> Scope<'a> {
    pub fn new(
        variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>,
        parent: Box<Scope<'a>>,
    ) -> Scope<'a> {
        return Scope {
            variables: variables,
            parent: parent,
        };
    }

    pub fn declare_variable(
        &mut self,
        name: &'a String,
        decltype: Box<BasicWrapper<'a>>,
        allow_casting: bool,
    ) -> &Box<BasicWrapper> {
        self.variables.insert(
            name,
            SymbolInfo::new(
                name,
                decltype,
                Box::new(BasicWrapper::from_value(Box::new(Null::new()))),
                allow_casting,
            ),
        );

        return &self.variables[name].value_wrapper;
    }

    // set_variable

    // find_variable_info

    // find_variable_value

    // find_variable_decltype

    // to_string
}
