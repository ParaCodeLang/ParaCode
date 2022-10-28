pub mod language {
    use std::fmt;
    use std::collections::HashMap;
    use std::ops::Deref;
    
    use crate::interpreter::basic_value::language::*;
    use crate::interpreter::basic_object::language::*;
    
    #[derive(Debug, Clone)]
    pub struct BasicType<'a> {
        pub basic_object: BasicObject<'a>,
    }
    
    impl fmt::Display for BasicType<'_> {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            return write!(f, "BasicType(ID: {}, Parent: {:?}, Members: {:?})", self.basic_object.id, self.basic_object.parent, self.basic_object.members);
        }
    }
    
    impl PartialEq<BasicType<'_>> for BasicType<'_> {
        fn eq(&self, _rhs: &BasicType<'_>) -> bool {
            return self.to_full_string() == _rhs.to_full_string();
        }

        fn ne(&self, _rhs: &BasicType<'_>) -> bool {
            return !(self == _rhs);
        }
    }
    impl PartialEq<BasicObject<'_>> for BasicType<'_> {
        fn eq(&self, _rhs: &BasicObject<'_>) -> bool {
            return self.to_full_string() == _rhs.to_full_string();
        }

        fn ne(&self, _rhs: &BasicObject<'_>) -> bool {
            return !(self == _rhs);
        }
    }
    impl PartialEq<dyn BasicValue> for BasicType<'_> {
        fn eq(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return self.to_full_string() == _rhs.to_full_string();
        }

        fn ne(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return !(self == _rhs);
        }
    }

    impl<'a> Deref for BasicType<'a> {
        type Target = BasicObject<'a>;
        fn deref(&self) -> &BasicObject<'a> {
            return &self.basic_object;
        }
    }

    impl<'a> BasicType<'a> {
        pub fn new(parent: Option<&'a Box<BasicObject<'a>>>, members: HashMap<String, Box<&'a dyn BasicValue>>) -> Self {
            return BasicType{
                basic_object: BasicObject::new(parent, members),
            };
        }

        pub fn parent(&mut self) -> Option<&Box<BasicObject>> {
            return self.basic_object.parent();
        }

        pub fn members(&mut self) -> Option<&HashMap<String, Box<&dyn BasicValue>>> {
            return self.basic_object.members();
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
            result.basic_object = result.basic_object.clone(parent_override);
            return result;
        }

        // assign_member
        pub fn assign_member(&mut self, name: String, value: Box<&'a dyn BasicValue>) {
            self.basic_object.assign_member(name, value);
        }

        // Needs BasicType
        // lookup_member

        // Needs BasicType
        // satisfies_type
    }

    impl<'a> BasicValue for BasicType<'a> {
        /*fn as_any(&self) -> &dyn std::any::Any {
            self
        }*/
        
        fn is_object(&self) -> bool {
            return true;
        }
        fn is_type(&self) -> bool {
            return true;
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


        /*fn parent(&mut self) -> Option<&Box<BasicObject>> {
            return self.basic_object.parent();
        }

        fn members(&mut self) -> Option<&HashMap<String, Box<&dyn BasicValue>>> {
            return self.basic_object.members();
        }*/

        // clone with parent_override

        // assign_member
        
        // Needs BasicType
        // lookup_member

        // Needs BasicType
        // satisfies_type
    }
    // crate::impl_basicvalue!(BasicType<'a>);
}
