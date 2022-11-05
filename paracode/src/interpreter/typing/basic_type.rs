use std::fmt;

#[derive(Debug)]
pub struct BasicType {}
impl BasicType {
    pub fn to_string(&self) -> String {
        return format!("{}", self);
    }

    pub fn get_detailed_string(&self) -> String {
        return format!("Type: BasicType, Value: {:?}", self);
    }
}
impl fmt::Display for BasicType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // TODO: Implement this.
        return write!(f, "BasicType");
    }
}