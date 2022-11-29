use std::fmt;
use std::collections::HashMap;

use crate::interpreter::basic_wrapper::BasicWrapper;

#[derive(Debug)]
pub struct ObjectMember<'a> {
    pub name: String,
    pub value: Box<BasicWrapper<'a>>,
}

#[derive(Debug)]
pub struct BasicObject<'a> {
    pub parent: Option<&'a Box<BasicWrapper<'a>>>, // Will be an object or type
    pub members: HashMap<&'a String, Box<BasicWrapper<'a>>>,
}
impl<'a> BasicObject<'a> {
    pub fn new(parent: Option<&'a Box<BasicWrapper<'a>>>, members: HashMap<&'a String, Box<BasicWrapper<'a>>>) -> BasicObject<'a> {
        return BasicObject {
            parent: parent,
            members: members,
        }
    }

    // Needs lookup_member
    // extract_value_member

    // lookup_type

    pub fn clone(&self, parent_override: Option<&'a Box<BasicWrapper<'a>>>) -> BasicObject<'a> {
        let mut members: HashMap<&String, Box<BasicWrapper>> = HashMap::new();
        for (name, value) in &self.members {
            members.insert(name, Box::new(BasicWrapper::clone(value, None)));
        }
        return BasicObject::new(match &parent_override {
            Some(_) => parent_override,
            None => self.parent,
        }, members);
    }

    // assign_member

    // Needs satisfies_type
    // lookup_member

    // satisfies_type

    pub fn is_type(&self) -> bool {
        return self.members.contains_key(&"name".to_string());
    }
    
    pub fn to_string(&self) -> String {
        return format!("{}", self);
    }

    pub fn get_detailed_string(&self) -> String {
        return format!("Type: BasicObject, Value: {:?}", self);
    }
}
impl<'a> fmt::Display for BasicObject<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // TODO: Implement this.
        return write!(f, "BasicObject");
    }
}
