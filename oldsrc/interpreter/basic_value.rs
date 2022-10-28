pub mod language {
    use std::fmt;
    use std::fmt::Debug;
    use std::collections::HashMap;
    use std::any::Any;

    // use downcast_rs::{Downcast};

    use crate::interpreter::basic_object::language::BasicObject;
    use crate::interpreter::typing::basic_type::language::BasicType;

    #[derive(Debug)]
    pub enum BasicVariant<'a> {
        Type(Box<BasicType<'a>>),
        Object(Box<BasicObject<'a>>),
        Value(Box<dyn BasicValue>),
        // TODO: Maybe move into BasicValue
        //Any(Any),
    }
    impl<'a> BasicVariant<'a> {
        pub const fn is_type(&self) -> bool {
            return matches!(*self, BasicVariant::Type(_));
        }
        pub const fn is_object(&self) -> bool {
            return matches!(*self, BasicVariant::Object(_));
        }
        pub const fn is_value(&self) -> bool {
            return matches!(*self, BasicVariant::Value(_));
        }

        pub fn unwrap_type(&self) -> &mut Box<BasicType<'a>> {
            match self {
                BasicVariant::Type(value) => value,
                BasicVariant::Object(_) => panic!("called `BasicVariant::unwrap_type()` but the stored value isn't of type `BasicObject`"),
                BasicVariant::Value(_) => panic!("called `BasicVariant::unwrap_type()` but the stored value isn't of type `BasicValue`"),
            }
        }
        pub fn unwrap_object(&self) -> &mut Box<BasicObject<'a>> {
            match self {
                BasicVariant::Type(_) => panic!("called `BasicVariant::unwrap_object()` but the stored value isn't of type `BasicType`"),
                BasicVariant::Object(value) => value,
                BasicVariant::Value(_) => panic!("called `BasicVariant::unwrap_object()` but the stored value isn't of type `BasicValue`"),
            }
        }
        pub fn unwrap_value(&self) -> &mut Box<dyn BasicValue + 'a> {
            match self {
                BasicVariant::Type(_) => panic!("called `BasicVariant::unwrap_object()` but the stored value isn't of type `BasicType`"),
                BasicVariant::Object(_) => panic!("called `BasicVariant::unwrap_object()` but the stored value isn't of type `BasicObject`"),
                // BasicVariant::Type(value) => value as Box<dyn BasicValue>,
                // BasicVariant::Object(value) => value as Box<dyn BasicValue>,
                BasicVariant::Value(value) => value,
            }
        }
        /*pub const fn unwrap<T>(self) -> Box<T> {
            let type_string = stringify!(T);
            if type_string == "BasicType" {
                return match self {
                    BasicVariant::Type(value) => value,
                    BasicVariant::Object(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicObject`", type_string),
                    BasicVariant::Value(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicValue`", type_string),
                };
            }
            else if type_string == "BasicObject" {
                return match self {
                    BasicVariant::Type(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicType`", type_string),
                    BasicVariant::Object(value) => value,
                    BasicVariant::Value(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicValue`", type_string),
                };
            }
            else {
                return match self {
                    BasicVariant::Type(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicType`", type_string),
                    BasicVariant::Object(_) => panic!("called `BasicVariant::unwrap<{}>()` but the stored value is of type `BasicObject`", type_string),
                    BasicVariant::Value(value) => value,
                };
            }
        }*/
    }
    
    pub trait BasicValue: /*Downcast + */Debug {
        // fn as_any<'a>(&self) -> &dyn Any where Self: 'a;
        
        fn is_object(&self) -> bool {
            return false;
        }
        /*fn as_object(&self) -> Option<BasicObject> {
            if self.is_object() {
                // return Some(unsafe { &self as BasicObject; }
                
                // let res = self.downcast::<Bar>();
                // if !res.is_err() {
                //     return Some(res.0);
                // }
                // return None;

                // if let Some(result) = self.downcast_ref::<BasicObject>() {
                //     return result;
                // }
                
                // return Some(self.downcast::<BasicObject>().map_err(|_| "Shouldn't happen.").unwrap().0);
            }
            return None;
        }*/
        fn is_type(&self) -> bool {
            return false;
        }
        /*fn as_type(&self) -> Option<BasicType> {
            if self.is_type() {
                return None;
            }
            return None;
        }*/
        
        fn compare_value(&self, other: Box<dyn BasicValue>) -> bool {
            return self.to_full_string() == other.to_full_string();
        }

        // fn extract_basicvalue(&self) -> Self {
        //     // TODO: Maybe change something here?
        //     return self;
        // }

        // fn extract_value(&self) -> Self {
        //     return self;
        // }

        // // lookup_type method

        fn is_null(&self) -> bool {
            return false;
        }

        fn clone(&self) -> Self where Self: Sized;

        fn to_string(&self) -> String;
        fn to_full_string(&self) -> String;


        /*// TODO: Add the BasicObject and BasicType methods but make them either return or do nothing.
        fn parent(&mut self) -> Option<&Box<BasicObject>> {
            return None;
        }

        fn members(&mut self) -> Option<&HashMap<String, Box<&dyn BasicValue>>> {
            return None;
        }*/

        // clone with parent_override

        // assign_member
        
        // Needs BasicType
        // lookup_member

        // Needs BasicType
        // satisfies_type
    }
    // impl_downcast!(BasicValue);

    impl fmt::Display for dyn BasicValue {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            return write!(f, "{}", self.to_string());
        }
    }

    #[macro_export]
    macro_rules! impl_basicvalue {
        ( $name:ident $(< $( $lt:tt $( : $clt:tt $(+ $dlt:tt )* )? ),+ >)? ) => {
            impl $(< $( $lt $( : $clt $(+ $dlt )* )? ),+ >)? BasicValue for $name $(< $( $lt ),+ >)? {
                /*fn as_any(&self) -> &dyn std::any::Any {
                    self
                }*/
                
                fn is_object(&self) -> bool {
                    return stringify!($name) == "BasicObject" || stringify!($name) == "BasicType";
                }
                fn is_type(&self) -> bool {
                    return stringify!($name) == "BasicType";
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
            }
        };
    }
    
    impl_basicvalue!(i32);
    impl_basicvalue!(f32);
    impl_basicvalue!(bool);
    impl_basicvalue!(String);
    
    impl<K, V, S> BasicValue for HashMap<K, V, S> where K: Clone + Debug, V: Clone + Debug, S: Clone + Debug {
        /*fn as_any(&self) -> &dyn std::any::Any {
            self
        }*/
        
        /*fn compare_value(&self, other: Box<dyn BasicValue>) -> bool {
            return self == other;
        }*/
        
        fn clone(&self) -> Self {
            return Clone::clone(self);
        }

        fn to_string(&self) -> String {
            return format!("{:?}", self);
        }

        fn to_full_string(&self) -> String {
            return format!("Type: {}, Value: {:?}", stringify!($typename), self);
        }
    }

    // Rust doesn't have a null type, so create a fake one.
    #[derive(Debug, Clone)]
    pub struct Null;
    impl fmt::Display for Null {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            return write!(f, "Null");
        }
    }
    impl PartialEq<dyn BasicValue> for Null {
        fn eq(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return self.is_null() && _rhs.is_null();
        }

        fn ne(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
            return !(self == _rhs);
        }
    }
    impl_basicvalue!(Null);
}
