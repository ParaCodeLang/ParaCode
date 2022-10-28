pub mod language {
    use crate::interpreter::basic_value::language::*;
    
    pub struct Stack {
        pub stack: Vec<Box<dyn BasicValue>>,
    }

    impl Default for Stack {
        fn default() -> Self {
            Self { stack: Vec::new(), }
        }
    }

    impl Stack {
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
    }
}
