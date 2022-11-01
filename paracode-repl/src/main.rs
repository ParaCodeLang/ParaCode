use std::env;

use paracode::paracode::ParaCode;

pub mod repl;

fn main() {
    let paracode = ParaCode::new();
    
    let args: Vec<String> = env::args().collect();
    if args.len() <= 1 {
        todo!("Run the repl");
        // paracode.repl();
        // return;
    }

    if args[1] == "--version" {
        println!("{}", paracode.version());
        return;
    }

    let filename = &args[1];
    todo!("Evaluate file: {}", filename);
    // paracode.evalFile(filename);
}
