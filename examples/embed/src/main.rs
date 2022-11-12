use paracode::paracode::ParaCode;

fn exampleEmbed(paracode: ParaCode) {
    paracode.callFunction("print", vec!["Hello from the embedding example!"]);
}

fn main() {
    let paracode = ParaCode::new();
    exampleEmbed(paracode);
}
