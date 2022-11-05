use std::collections::HashMap;
use std::fmt;
use std::fmt::Debug;

//use crate::interpreter::basic_object::BasicObject;
//use crate::interpreter::typing::basic_type::BasicType;

pub trait BasicValue: Debug {
    fn compare_value(&self, other: Box<dyn BasicValue>) -> bool {
        return self.get_detailed_string() == other.get_detailed_string();
    }

    // Needs BasicType
    // lookup_type

    fn is_null(&self) -> bool {
        return false;
    }

    fn is_object(&self) -> bool {
        return false;
    }

    fn clone(&self) -> Self where Self: Sized;

    fn to_string(&self) -> String;
    fn get_detailed_string(&self) -> String;
}

impl fmt::Display for dyn BasicValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", self.to_string());
    }
}

#[macro_export]
macro_rules! impl_basicvalue {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl $(< $( $lt $( : $clt $(+ $dlt )* )? ),+ >)? BasicValue for $name $(< $( $lt ),+ >)? {
            fn is_null(&self) -> bool {
                return stringify!($name) == "Null";
            }

            fn is_object(&self) -> bool {
                return stringify!($name) == "Empty";
            }


            fn clone(&self) -> Self {
                return Clone::clone(self);
            }

            fn to_string(&self) -> String {
                return format!("{}", self);
            }

            fn get_detailed_string(&self) -> String {
                return format!("Type: {}, Value: {:?}", stringify!($name), self);
            }
        }
    };
}

impl_basicvalue!(i32);
impl_basicvalue!(f32);
impl_basicvalue!(bool);
impl_basicvalue!(String);

// TODO: Try to move the "where ..." into the macro
impl<K, V, S> BasicValue
    for HashMap<K, V, S>
    where K: Clone + Debug, V: Clone + Debug, S: Clone + Debug
{
    fn clone(&self) -> Self {
        return Clone::clone(self);
    }

    fn to_string(&self) -> String {
        return format!("{:?}", self);
    }

    fn get_detailed_string(&self) -> String {
        return format!("Type: HashMap, Value: {:?}", self);
    }
}

// TODO: Try to move the "where ..." into the macro
impl<T> BasicValue for Vec<T> where T: Clone + Debug {
    fn clone(&self) -> Self {
        return Clone::clone(self);
    }

    fn to_string(&self) -> String {
        return format!("{:?}", self);
    }

    fn get_detailed_string(&self) -> String {
        return format!("Type: Vec, Value: {:?}", self);
    }
}

// Rust doesn't have a null type, so create a fake one.
#[derive(Debug, Clone)]
pub struct Null;
impl Null {
    pub fn new() -> Self {
        return Self {};
    }
}
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

#[derive(Debug, Clone)]
pub struct Empty;
impl Empty {
    pub fn new() -> Self {
        return Self {};
    }
}
impl fmt::Display for Empty {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "Empty");
    }
}
impl PartialEq<dyn BasicValue> for Empty {
    fn eq(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
        return self.is_object() && _rhs.is_object();
    }

    fn ne(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
        return !(self == _rhs);
    }
}
impl_basicvalue!(Empty);