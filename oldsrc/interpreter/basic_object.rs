pub mod language {
    use std::fmt;
    use std::collections::HashMap;
    
    use uuid::Uuid;
    
    use crate::interpreter::basic_value::language::*;

    #[derive(Debug, Clone)]
    pub struct ObjectMember<'a> {
        pub name: String,
        pub value: Box<&'a dyn BasicValue>,
    }
    
    #[derive(Debug, Clone)]
    pub struct BasicObject<'a> {
        pub parent: Option<&'a Box<BasicObject<'a>>>,
        pub members: HashMap<String, Box<&'a dyn BasicValue>>,
        // An internal ID used to identify the object and tell it apart from other BasicObjects.
        pub id: Uuid,
        // Rust doesn't have struct inheritence, so we're keeping track of the BasicType object, which sadly won't be represented as a derivitave of BasicObject.
        //pub type_object: Option<&'a BasicType>,
    }
    
    impl fmt::Display for BasicObject<'_> {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            return write!(f, "BasicObject(ID: {}, Parent: {:?}, Members: {:?})", self.id, self.parent, self.members);
        }
    }
    
    impl PartialEq<BasicObject<'_>> for BasicObject<'_> {
        fn eq(&self, _rhs: &BasicObject<'_>) -> bool {
            return self.to_full_string() == _rhs.to_full_string();
        }

        fn ne(&self, _rhs: &BasicObject<'_>) -> bool {
            return !(self == _rhs);
        }
    }
    impl PartialEq<dyn BasicValue> for BasicObject<'_> {
        fn eq(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return self.to_full_string() == _rhs.to_full_string();
        }

        fn ne(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return !(self == _rhs);
        }
    }

    impl<'a> BasicObject<'a> {
        pub fn new(parent: Option<&'a Box<BasicObject<'a>>>, members: HashMap<String, Box<&'a dyn BasicValue>>) -> Self {
            return BasicObject{
                parent: parent,
                members: members,
                //type_object: None,
                id: Uuid::new_v4()
            };
        }

        pub fn parent(&mut self) -> Option<&'a Box<BasicObject<'a>>> {
            return self.parent;
        }

        pub fn members(&mut self) -> Option<&HashMap<String, Box<&'a dyn BasicValue>>> {
            return Some(&self.members);
        }
        
        // Needs lookup_member
        /*pub fn extract_value_member(self: Self) -> Box<&'a dyn BasicValue> {
            if self.lookup_member("_value") {
                return self.lookup_member("_value").value;
            }
            return self;
        }*/

        // lookup_type
        
        pub fn clone(&self, parent_override: Option<&'a Box<BasicObject<'a>>>) -> Self {
            let mut result: Self = BasicValue::clone(self);
            result.parent = match parent_override {
                Some(_) => parent_override,
                None => self.parent,
            };
            // result.parent = parent_override.unwrap_or(self.parent);
            result.id = Uuid::new_v4();
            return result;
        }

        // assign_member
        pub fn assign_member(&mut self, name: String, value: Box<&'a dyn BasicValue>) {
            self.members.insert(name, value);
        }

        // Needs BasicType
        // lookup_member

        // Needs BasicType
        // satisfies_type
    }

    impl<'a> BasicValue for BasicObject<'a> {
        /*fn as_any(&self) -> &dyn std::any::Any {
            self
        }*/
        
        fn is_object(&self) -> bool {
            return true;
        }
        fn is_type(&self) -> bool {
            return false;
        }
        
        /*fn compare_value(&self, other: Box<dyn BasicValue>) -> bool {
            return self == other;
        }*/

        fn is_null(&self) -> bool {
            return stringify!($name) == "Null";
        }
        
        fn clone(&self) -> Self {
            return Clone::clone(self);
        }

        fn to_string(&self) -> String {
            return format!("{}", self);
        }

        fn to_full_string(&self) -> String {
            return format!("Type: {}, Value: {:?}", stringify!($name), self);
        }


        /*fn parent(&mut self) -> Option<&'a Box<BasicObject<'a>>> {
            return self.parent;
        }

        fn members(&mut self) -> Option<&HashMap<String, Box<&'a dyn BasicValue>>> {
            return Some(&self.members);
        }*/

        // clone with parent_override

        // assign_member
        
        // Needs BasicType
        // lookup_member

        // Needs BasicType
        // satisfies_type
    }
    // crate::impl_basicvalue!(BasicObject<'a>);
}
