use uuid::Uuid;

use crate::interpreter::basic_object::BasicObject;
use crate::interpreter::basic_value::{BasicValue, ObjectStub};

#[derive(Debug)]
pub struct BasicWrapper<'a> {
    pub value: Box<dyn BasicValue>,
    pub object: Option<Box<BasicObject<'a>>>,

    uuid: Uuid,
}
impl<'a> BasicWrapper<'a> {
    pub fn from_value(value: Box<dyn BasicValue>) -> BasicWrapper<'a> {
        return BasicWrapper {
            value: value,
            object: None,
            uuid: Uuid::new_v4(),
        };
    }

    pub fn from_object(object: Box<BasicObject<'a>>) -> BasicWrapper<'a> {
        return BasicWrapper {
            value: Box::new(ObjectStub::new()),
            object: Some(object),
            uuid: Uuid::new_v4(),
        };
    }

    pub fn is_object(&self) -> bool {
        return match self.object {
            Some(_) => true,
            None => false,
        };
    }

    pub fn is_type(&self) -> bool {
        return match &self.object {
            Some(object) => object.is_type(),
            None => false,
        };
    }

    pub fn is_null(&self) -> bool {
        return self.value.is_null();
    }

    pub fn clone(&self, parent_override: Option<&'a Box<BasicWrapper<'a>>>) -> BasicWrapper<'a> {
        if self.is_object() {
            return BasicWrapper::from_object(match &self.object {
                Some(object) => Box::new(BasicObject::clone(object, parent_override)),
                None => unreachable!(),
            });
        }
        return BasicWrapper::from_value(self.value.clone());
    }

    pub fn to_string(&self) -> String {
        if self.is_object() {
            return self.object.as_ref().unwrap().to_string();
        } else {
            return self.value.to_string();
        }
    }

    pub fn get_detailed_string(&self) -> String {
        if self.is_object() {
            return self.object.as_ref().unwrap().get_detailed_string();
        } else {
            return self.value.get_detailed_string();
        }
    }

    pub fn compare_value(&self, other: &'a Box<BasicWrapper<'a>>) -> bool {
        return self.get_detailed_string() == other.get_detailed_string();
    }

    pub fn get_uuid(&self) -> Uuid {
        return self.uuid;
    }
}
impl<'a> PartialEq<BasicWrapper<'a>> for BasicWrapper<'a> {
    fn eq(&self, _rhs: &BasicWrapper<'a>) -> bool {
        return self.get_detailed_string() == _rhs.get_detailed_string();
    }

    fn ne(&self, _rhs: &BasicWrapper<'a>) -> bool {
        return !(self == _rhs);
    }
}
