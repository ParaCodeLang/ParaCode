pub mod language {
    use crate::interpreter::basic_value::language::*;
    use crate::interpreter::basic_object::language::*;

    pub struct SymbolInfo {
        // pub varname: String,
        // // pub decltype: BasicType,
        // pub value_wrapper: Box<dyn BasicValue>,
        // pub allow_casting: bool,
    }
    impl SymbolInfo {
        // pub fn new(varname: &str, /*decltype: BasicType, */value: Box<dyn BasicValue>, allow_casting: bool) -> SymbolInfo {
        // }
    }

    /*pub struct Scope {
        pub stack: Vec<Box<dyn BasicValue>>,
    }

    impl Default for Scope {
        fn default() -> Self {
            Self { stack: Vec::new(), }
        }
    }

    impl Scope {
        fn push(&mut self, value: Box<dyn BasicValue>) {
            self.stack.push(value);
        }
        
        fn pop(&mut self) -> Box<dyn BasicValue> {
            let val = self.stack.pop();
            match val {
                Some(p) => return p,
                None => return Box::new(Null{}),
            }
        }
    }*/
}
