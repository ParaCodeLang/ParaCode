use std::env;
use std::collections::HashMap;
use std::any::Any;

use crate::paracode::language::*;
use crate::interpreter::basic_value::language::*;
use crate::interpreter::basic_object::language::*;
use crate::interpreter::typing::basic_type::language::*;
use crate::interpreter::stack::language::*;
use crate::interpreter::scope::language::*;
use crate::interpreter::variable::language::*;

// #[macro_use]
// extern crate downcast_rs;

// #[macro_use]
// extern crate better_any;

mod paracode;
mod interpreter;

fn main() {
    // let answer = 42;
    // let maybe_pi = 3.14;
    // let v: Vec<&dyn BasicValue> = vec![&answer, &maybe_pi];
    // for d in v.iter() {
    //     println!("{}", d.to_string());
    //     println!("{}", d.clone());
    // }
    
    // let bv: &dyn BasicValue = &1;
    // println!("{}", bv);

    let mut a: BasicVariant = BasicVariant::Value(Box::new(42));
    let mut b: BasicVariant = BasicVariant::Object(Box::new(BasicObject::new(None, HashMap::new())));
    let mut c: BasicVariant = BasicVariant::Type(Box::new(BasicType::new(None, HashMap::new())));
    // let mut q: BasicVariant = BasicVariant::Object(Box::new(BasicObject::new(None, HashMap::new())));
    // let mut c: BasicVariant = BasicVariant::Type(Box::new(BasicType::new(Some(&q.unwrap_object()), HashMap::new())));
    let mut v: Vec<&BasicVariant> = vec![&a, &b, &c];
    println!("{:?}\n", v);

    println!("{}", (HashMap::<i32, i32>::new()).is_object());
    println!("{}", (HashMap::<i32, i32>::new()).is_type());
    //println!("{:?}", (HashMap::<i32, i32>::new()).parent());
    //println!("{:?}", (HashMap::<i32, i32>::new()).members());
    println!("{}", a.unwrap_value().is_object());
    println!("{}", a.unwrap_value().is_type());
    //println!("{:?}", a.parent());
    //println!("{:?}", a.members());
    println!("{}", b.unwrap_object().is_object());
    println!("{}", b.unwrap_object().is_type());
    println!("{:?}", b.unwrap_object().parent());
    println!("{:?}", b.unwrap_object().members());
    println!("{}", c.unwrap_type().is_object());
    println!("{}", c.unwrap_type().is_type());
    println!("{:?}", c.unwrap_type().parent());
    println!("{:?}", c.unwrap_type().members());
    println!();

    // let mut b2: Box<dyn Any> = b;
    // let mut d: Box<dyn BasicValue> = match c.as_any().downcast_ref::<BasicType>() {
    //     Some(i) => i,
    //     None => panic!(),
    // };
    // println!("{:?}", d);
    
    // let mut e: Box<dyn BasicValue> = match c.as_any().downcast_ref::<BasicType>() {
    //     Some(i) => i,
    //     None => panic!(),
    // }.basic_object;
    // println!("{:?}", e);
    
    // let mut f: Box<dyn BasicValue> = match c.as_any().downcast_ref::<BasicObject>() {
    //     Some(i) => i,
    //     None => panic!(),
    // };
    // println!("{:?}", f);
    
    let paracode = ParaCode { ..Default::default() };
    
    let args: Vec<String> = env::args().collect();
    if args.len() <= 1 {
        todo!("Run the repl");
        // paracode.repl();
        // return;
    }

    if args[1] == "--version" {
        println!("{}", paracode.version);
        return;
    }

    let filename = &args[1];
    todo!("Evaluate file: {}", filename);
    // paracode.evalFile(filename);
}
