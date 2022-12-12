use crate::interpreter::basic_wrapper::BasicWrapper;

pub struct BasicTyping {}
impl BasicTyping {
    pub fn repr_function_name() -> String {
        return "to_str".to_string();
    }

    pub fn type_name<'a>(type_obj: &'a Box<BasicWrapper<'a>>) -> String {
        return match &type_obj.object {
            Some(object) => {
                match object.members.get(&"name".to_string()) {
                    Some(name) => name.to_string(),
                    None => "".to_string(),
                }
            },
            None => "".to_string(),
        };
    }

    pub fn friendly_typename<'a>(type_obj: &'a Box<BasicWrapper<'a>>) -> String {
        if let Some(object) = &type_obj.object {
            if let Some(name) = object.members.get(&"name".to_string()) {
                if let Some(inner_object) = &name.object {
                    return inner_object.to_string();
                } else {
                    return name.to_string();
                }
            }
        }
    
        return format!("{:?}", type_obj);
    }

    pub fn compare_type<'a>(
        type_obj: &'a Box<BasicWrapper<'a>>,
        other_type: &'a Box<BasicWrapper<'a>>,
        parent_lookup: bool
    ) -> bool {
        if other_type == type_obj {
            return true;
        }
    
        if type_obj.compare_value(other_type) {
            return true;
        }
    
        if let Some(type_object) = &type_obj.object {
            if let Some(other_type_object) = &other_type.object {
                if parent_lookup && type_object.parent.is_some() {
                    if let Some(other_type_parent) = &other_type_object.parent.as_ref().unwrap().object {
                        let circular = other_type_parent.parent == Some(&other_type);
                
                        return BasicTyping::compare_type(type_object.parent.unwrap(), other_type_object.parent.unwrap(), !circular);
                    }
                }
            }
        }
    
        return false;
    }

    pub fn has_property<'a>(
        type_obj: &'a Box<BasicWrapper<'a>>,
        name: &'a String,
        property_type: Option<&'a Box<BasicWrapper<'a>>>,
        limit: bool
    ) -> bool {
        if let Some(object) = &type_obj.object {
            if object.members.contains_key(name) {
                return true;
            }
    
            if limit || object.parent.is_none() {
                return false;
            }
    
            return BasicTyping::has_property(object.parent.as_ref().unwrap(), name, property_type, limit);
        }
    
        return false;
    }

    pub fn get_property_type<'a>(
        type_obj: &'a Box<BasicWrapper<'a>>,
        name: &'a String,
        limit: bool,
    ) -> Option<&'a Box<BasicWrapper<'a>>> {
        if let Some(object) = &type_obj.object {
            if object.members.contains_key(name) {
                return Some(&object.members[name]);
            }
            if limit || object.parent.is_none() {
                return None;
            }
            if let Some(parent) = &object.parent {
                return BasicTyping::get_property_type(parent, name, limit);
            }
        }
        return None;
    }
}
