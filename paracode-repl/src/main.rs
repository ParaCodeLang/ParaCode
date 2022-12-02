use std::env;

use paracode::paracode::ParaCode;

use crate::repl::Repl;

pub mod repl;

#[quit::main]
fn main() {
    let paracode = ParaCode::new();

    let args: Vec<String> = env::args().collect();
    if args.len() <= 1 {
        let mut repl = Repl::new(paracode);
        repl.run();
        return;
    }

    if args[1] == "--version" {
        println!("{}", paracode.version());
        return;
    }

    let filename = &args[1];
    todo!("Evaluate file: {}", filename);
    // paracode.evalFile(filename);
}
