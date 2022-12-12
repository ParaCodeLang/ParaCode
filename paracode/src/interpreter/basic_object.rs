use std::collections::HashMap;
use std::fmt;

use crate::interpreter::basic_wrapper::BasicWrapper;
use crate::interpreter::basic_value::BasicValue;

#[derive(Debug)]
pub struct ObjectMember<'a> {
    pub name: &'a String,
    pub value: &'a Box<BasicWrapper<'a>>,
}
impl<'a> ObjectMember<'a> {
    pub fn new(name: &'a String, value: &'a Box<BasicWrapper<'a>>) -> ObjectMember<'a> {
        return ObjectMember {
            name: name,
            value: value
        };
    }
}

#[derive(Debug, PartialEq)]
pub struct BasicObject<'a> {
    pub parent: Option<&'a Box<BasicWrapper<'a>>>, // Will be an object or type
    pub members: HashMap<&'a String, Box<BasicWrapper<'a>>>,
}
impl<'a> BasicObject<'a> {
    pub fn new(
        parent: Option<&'a Box<BasicWrapper<'a>>>,
        members: HashMap<&'a String, Box<BasicWrapper<'a>>>,
    ) -> BasicObject<'a> {
        return BasicObject {
            parent: parent,
            members: members,
        };
    }

    // extract_value_member
    // pub fn extract_value_member(&self) -> Option<&'a Box<dyn BasicValue>> {
    //     if let Some(member) = self.lookup_member(&"_value".to_string(), None, true) {
    //         let value = member.value;
    //         return Some(value.value);
    //     }
    //     return None;
    // }


    // lookup_type

    pub fn clone(&self, parent_override: Option<&'a Box<BasicWrapper<'a>>>) -> BasicObject<'a> {
        let mut members: HashMap<&String, Box<BasicWrapper>> = HashMap::new();
        for (name, value) in &self.members {
            members.insert(name, Box::new(BasicWrapper::clone(value, None)));
        }
        return BasicObject::new(
            match &parent_override {
                Some(_) => parent_override,
                None => self.parent,
            },
            members,
        );
    }

    // assign_member

    pub fn lookup_member<'b>(
        &'b self,
        name: &'a String,
        member_type: Option<&'a Box<BasicWrapper<'a>>>,
        parent_lookup: bool,
    ) -> Option<ObjectMember<'b>> {
        if self.members.contains_key(name) {
            if let Some(member) = self.members.get(name) {
                if let Some(object) = &member.object {
                    if member_type.is_none() || object.satisfies_type(member_type.unwrap()) {
                        return Some(ObjectMember::new(name, member));
                    }
                }
            }
        }
    
        if parent_lookup && self.parent.is_some() {
            if let Some(object) = &self.parent.unwrap().object {
                return object.lookup_member(name, member_type, parent_lookup);
            }
        }
        return None;
    }

    pub fn satisfies_type(&self, ty: &'a Box<BasicWrapper<'a>>) -> bool {
        if let Some(object) = &ty.object {
            // All members are String -> BasicObject (or an extension thereof)
            for (tname, tvalue) in object.members.iter() {
                if self.lookup_member(tname, Some(tvalue), true).is_none() {
                    return false;
                }
            }
    
            if object.parent.is_some() {
                return self.satisfies_type(&object.parent.unwrap());
            }
        }

        return true;
    }

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
