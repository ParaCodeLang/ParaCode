use crate::interpreter::basic_wrapper::BasicWrapper;

#[derive(Debug)]
pub struct Stack<'a> {
    pub stack: Vec<Box<BasicWrapper<'a>>>,
}
impl<'a> Stack<'a> {
    pub fn new(stack: Vec<Box<BasicWrapper<'a>>>) -> Stack<'a> {
        return Stack {
            stack: stack,
        };
    }
    
    pub fn push(&mut self, value: Box<BasicWrapper<'a>>) {
        self.stack.push(value);
    }
    
    pub fn pop(&mut self) -> Option<Box<BasicWrapper<'a>>> {
        return self.stack.pop();
    }
}
