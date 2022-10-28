use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum BasicValue {
    Int(i32),
    Float(f32),
    Null,
    // TODO: Add BasicObject and BasicType
    // TODO: Add an extension point for user-defined types
}

impl fmt::Display for BasicValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Int(n) => write!(f, "{}", n),
            Self::Float(n) => write!(f, "{}", n),
            Self::Null => write!(f, "Null"),
        }
    }
}
