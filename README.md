# ParaCode
### Prototypical language with knack for extensibility and meta programming

**This is the official Rust port of ParaCode. It is currently incomplete. You can find the current status of the project at [the Trello board](https://trello.com/b/Nxs0bt1f/paracode-rust).**

In ParaCode, all types are objects, and vice versa. Everything is an object, and that includes functions. Objects descend from a parent object and inherit functions and variables from the parent. For example, to create a type, we extend from a parent `Object` (in this case `Type`), and define any methods

The core library in ParaCode is written in itself, even allowing for methods to be attached with the `Object.patch()` method at runtime. Types in ParaCode are built of `Object`s and have overloadable functions for operations such as addition, subtraction, multiplication, division, modulus, and compare. Types including String, Int, Float, and Bool are all defined completely in ParaCode, including all operations that can be done on them. For instance, the call operator can be overloaded, with an example being that when a Number is called `5(10)` it multiplies the values together, allowing for a math-like syntax in programming.

ParaCode also has many methods that have functional language characteristics for example Array mapping and lambdas, and new concept ideas such as [Prototypical Inheritance](https://en.wikipedia.org/wiki/Prototype-based_programming). 

I'm currently rewriting ParaCode in Rust for better speed and efficiency. I'm planning to keep ParaCode code and the standard library similar to how it is today, and even try maintaining version parity unless it becomes too much of a burden on me and the language itself.

[vars](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/00_vars.md) - How to declare and use variables

[functions](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/10_functions.md) - Writing and calling functions

[strings](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/15_strings.md) - Strings operations and interpolation

[operators](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/16_operators.md) - Available operators + Operator overloading

[types](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/20_types.md) - Custom types

[proto](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/30_proto.md) - Extending types using prototypical inheritance

[macros](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/35_macros.md) - Macros

[arrays](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/40_arrays.md) - Array operations

[dictionary](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/41_dictionary.md) - Dictionary operations

[iterators](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/50_iterators.md) - Building custom iterator objects

[random](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/55_random.md) - Random number generation

[modules](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/60_modules.md) - Modules

[packages](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/61_packages.md) - Packages

[console](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/70_console.md) - Console input and output

[files](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-cpo/doc/80_files.md) - File reading and writing

[json](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/doc/81_json.md) - JSON reading and writing


### Examples

[embedding](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/embed.rs)

[numbers](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/numbers.para)

[strings](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/string.para)

[patching](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/patching.para)

[operator overloading](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/operator_overloading.para)

[tic tac toe](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/ttt.para)

[pythagorean theorem calculator](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/pythagorean.para)

[rule110](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/examples/rule110.para)

Be sure to check out our TicTacToe example!
Start the REPL by running `main.py` and call `tictactoe();` to try it out!

To update ParaCode, run the `update.sh` file located in the `scripts` directory. On most operating systems this can be done with
```shell
sh scripts/update.sh
```
Or, to install and update ParaCode, run everything from `update.sh`.

You can find the [Changelog](https://github.com/ParaCodeLang/ParaCode/blob/rewrite-rust/CHANGELOG.md) here.
