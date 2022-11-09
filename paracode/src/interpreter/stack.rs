use crate::interpreter::basic_wrapper::BasicWrapper;

pub struct Stack {
    pub stack: Vec<Box<BasicWrapper>>,
}
impl Stack {
    pub fn new(stack: Vec<Box<BasicWrapper>>) -> Stack {
        return Stack {
            stack: stack,
        };
    }
    
    pub fn push(&mut self, value: Box<BasicWrapper>) {
        self.stack.push(value);
    }
    
    pub fn pop(&mut self) -> Option<Box<BasicWrapper>> {
        return self.stack.pop();
    }
}
