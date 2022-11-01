use paracode::paracode::ParaCode;

fn exampleEmbed(paracode: ParaCode) {
    paraCode.callFunction("print", vec!["Hello from the embedding example!"]);
}
