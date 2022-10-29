use std::fmt;
// use std::collections::HashMap;

use crate::interpreter::std::float32::Float32;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum BasicValue {
    Int(i32),
    // Use of a custom float wrapper instead of the primitive type is necesary for hash support, and may be removed later
    Float(Float32),
    Bool(bool),
    String(String),
    // TODO: Either get dictionaries to work or remove the below line
    // Dictionary(HashMap<BasicValue, BasicValue>),
    Array(Vec<BasicValue>),
    Null,
    // TODO: Add BasicObject and BasicType
    // TODO: Add an extension point for user-defined types
}
impl BasicValue {
    pub fn is_null(&self) -> bool {
        return self == &BasicValue::Null;
    }
}

impl fmt::Display for BasicValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Int(val) => write!(f, "{}", val),
            Self::Float(val) => write!(f, "{}", val),
            Self::Bool(val) => write!(f, "{}", val),
            Self::String(val) => write!(f, "{}", val),
            // Self::Dictionary(val) => write!(f, "{:?}", val),
            Self::Array(val) => write!(f, "{:?}", val),
            Self::Null => write!(f, "Null"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn custom_float_addition() {
      assert_eq!(Float32::new(1.4) + 2.1, Float32::new(1.4 + 2.1));
    }

    #[test]
    fn null_is_null() {
      assert_eq!(BasicValue::Null.is_null(), true);
    }

    #[test]
    fn is_null() {
      assert_eq!(BasicValue::Int(1).is_null(), false);
    }
}
