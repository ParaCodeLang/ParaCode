use std::collections::HashMap;
use std::fmt;
use std::fmt::Debug;

use downcast_rs::Downcast;
use dyn_clone::DynClone;

pub trait BasicValue: Debug + DynClone + Downcast {
    fn compare_value(&self, other: Box<dyn BasicValue>) -> bool {
        return self.get_detailed_string() == other.get_detailed_string();
    }

    // lookup_type

    fn is_null(&self) -> bool {
        return false;
    }

    fn is_object(&self) -> bool {
        return false;
    }

    fn to_string(&self) -> String;
    fn get_detailed_string(&self) -> String;
}
impl fmt::Display for dyn BasicValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", self.to_string());
    }
}
dyn_clone::clone_trait_object!(BasicValue);
impl_downcast!(BasicValue);

#[macro_export]
macro_rules! impl_basicvalue {
    ($name:ident $(< $($lt:tt $(: $clt:tt $(+ $dlt:tt)*)?),+ >)?) => {
        impl $(< $( $lt $( : $clt $(+ $dlt )* )? ),+ >)? BasicValue for $name $(< $( $lt ),+ >)? {
            fn is_null(&self) -> bool {
                return stringify!($name) == "Null";
            }

            fn is_object(&self) -> bool {
                return stringify!($name) == "ObjectStub";
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

impl<K, V, S> BasicValue for HashMap<K, V, S>
where
    K: Clone + Debug + 'static,
    V: Clone + Debug + 'static,
    S: Clone + Debug + 'static,
{
    fn to_string(&self) -> String {
        return format!("{:?}", self);
    }

    fn get_detailed_string(&self) -> String {
        return format!("Type: HashMap, Value: {:?}", self);
    }
}

impl<T> BasicValue for Vec<T>
where
    T: Clone + Debug + 'static,
{
    fn to_string(&self) -> String {
        return format!("{:?}", self);
    }

    fn get_detailed_string(&self) -> String {
        return format!("Type: Vec, Value: {:?}", self);
    }
}

// Rust doesn't have a null type, so create a fake one.
#[derive(Debug, Clone)]
pub struct Null {}
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

// A type to be stored in BasicWrapper with BasicObjects
#[derive(Debug, Clone)]
pub struct ObjectStub {}
impl ObjectStub {
    pub fn new() -> Self {
        return Self {};
    }
}
impl fmt::Display for ObjectStub {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "ObjectStub");
    }
}
impl PartialEq<dyn BasicValue> for ObjectStub {
    fn eq(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
        return self.is_object() && _rhs.is_object();
    }

    fn ne(&self, _rhs: &(dyn BasicValue + 'static)) -> bool {
        return !(self == _rhs);
    }
}
impl_basicvalue!(ObjectStub);

#[cfg(test)]
mod tests {
    use crate::interpreter::basic_value::BasicValue;

    #[cfg(test)]
    use pretty_assertions::assert_eq;

    #[test]
    fn cast_checking() {
        let mut basic_val: Box<dyn BasicValue> = Box::new(127);

        assert_eq!(basic_val.is::<i32>(), true);
        assert_eq!(basic_val.is::<f32>(), false);
    }

    #[test]
    fn casting() {
        let mut basic_val: Box<dyn BasicValue> = Box::new(127);

        if let Some(real_val) = basic_val.downcast_ref::<i32>() {
            assert_eq!(real_val, &127);
        }
    }
}
