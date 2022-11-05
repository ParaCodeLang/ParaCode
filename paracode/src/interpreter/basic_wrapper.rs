use crate::interpreter::basic_value::{ BasicValue, Empty };
use crate::interpreter::basic_object::BasicObject;
use crate::interpreter::typing::basic_type::BasicType;

#[derive(Debug)]
pub struct BasicWrapper {
    value: Box<dyn BasicValue>,
    object: Option<Box<BasicObject>>,
    type_object: Option<Box<BasicType>>,
}
impl BasicWrapper {
    pub fn from_value(value: Box<dyn BasicValue>) -> BasicWrapper {
        return BasicWrapper {
            value: value,
            object: None,
            type_object: None,
        };
    }

    pub fn from_object(object: Box<BasicObject>) -> BasicWrapper {
        return BasicWrapper {
            value: Box::new(Empty::new()),
            object: Some(object),
            type_object: None,
        };
    }

    pub fn from_type(object: Box<BasicObject>, type_object: Box<BasicType>) -> BasicWrapper {
        return BasicWrapper {
            value: Box::new(Empty::new()),
            object: Some(object),
            type_object: Some(type_object),
        };
    }

    pub fn is_object(&self) -> bool {
        return match self.object {
            Some(_) => true,
            None => false,
        };
    }

    pub fn is_type(&self) -> bool {
        return match self.type_object {
            Some(_) => true,
            None => false,
        };
    }

    pub fn is_null(&self) -> bool {
        return self.value.is_null();
    }

    pub fn to_string(&self) -> String {
        if self.is_type() {
            return self.type_object.as_ref().unwrap().to_string();
        } else if self.is_object() {
            return self.object.as_ref().unwrap().to_string();
        } else {
            return self.value.to_string();
        }
    }

    pub fn get_detailed_string(&self) -> String {
        if self.is_type() {
            return self.type_object.as_ref().unwrap().get_detailed_string();
        } else if self.is_object() {
            return self.object.as_ref().unwrap().get_detailed_string();
        } else {
            return self.value.get_detailed_string();
        }
    }

    pub fn compare_value(&self, other: Box<BasicWrapper>) -> bool {
        return self.get_detailed_string() == other.get_detailed_string();
    }
}