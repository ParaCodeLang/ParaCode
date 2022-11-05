use std::fmt;

use uuid::Uuid;

#[derive(Debug)]
pub struct BasicObject {}
impl BasicObject {
    pub fn to_string(&self) -> String {
        return format!("{}", self);
    }

    pub fn get_detailed_string(&self) -> String {
        return format!("Type: BasicObject, Value: {:?}", self);
    }
}
impl fmt::Display for BasicObject {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // TODO: Implement this.
        return write!(f, "BasicObject");
    }
}