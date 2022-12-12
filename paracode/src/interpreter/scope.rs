use std::collections::HashMap;
use std::fmt;

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

pub struct Scope<'a> {
    pub variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>,
    pub parent: Option<Box<Scope<'a>>>,
}
impl<'a> Scope<'a> {
    pub fn new(
        variables: &'a mut HashMap<&'a String, SymbolInfo<'a>>,
        parent: Option<Box<Scope<'a>>>,
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

    pub fn set_variable(&mut self, name: &'a String, value: Box<BasicWrapper<'a>>) {
        if let Some(_) = self.find_variable_info(name, false) {
            let var_ref = self.variables.get_mut(name).unwrap(); // Get a mutable reference to the variable in the scope's variables map.
            var_ref.value_wrapper = value; // Set the value of the variable.
        }
    }

    pub fn find_variable_info<'b>(
        &'b mut self,
        name: &'a String,
        limit: bool,
    ) -> Option<&'b SymbolInfo<'a>> {
        if self.variables.contains_key(name) {
            return Some(&self.variables[name]);
        }

        if !limit && self.parent.is_some() {
            return self
                .parent
                .as_mut()
                .unwrap()
                .find_variable_info(name, false);
        }

        return None;
    }

    pub fn find_variable_value<'b>(
        &'b mut self,
        name: &'a String,
        limit: bool,
    ) -> Option<&'b Box<BasicWrapper<'a>>> {
        let variable_info = self.find_variable_info(name, limit);
        if variable_info.is_some() {
            return Some(&variable_info.unwrap().value_wrapper);
        }
        return None;
    }

    pub fn find_variable_decltype<'b>(
        &'b mut self,
        name: &'a String,
        limit: bool,
    ) -> Option<&'b Box<BasicWrapper<'a>>> {
        let variable_info = self.find_variable_info(name, limit);
        if variable_info.is_some() {
            return Some(&variable_info.unwrap().decltype);
        }
        return None;
    }
}
impl<'a> fmt::Display for Scope<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "Scope definitions: {:?}", self.variables);
    }
}
impl<'a> fmt::Debug for Scope<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", self);
    }
}
