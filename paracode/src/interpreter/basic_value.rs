use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum BasicValue {
    Int(i32),
    Float(f32),
    Bool(bool),
    String(String),
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
            Self::Null => write!(f, "Null"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn null_is_null() {
      assert_eq!(BasicValue::Null.is_null(), true);
    }

    #[test]
    fn is_null() {
      assert_eq!(BasicValue::Int(1).is_null(), false);
    }
}
