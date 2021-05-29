# ParaCode
### Prototypical language with knack for extensibility and meta programming

In ParaCode, all types are objects, and vice versa. Everything is an object, and that includes functions. Objects descend from a parent object and inherit functions and variables from the parent. For example, to create a type, we extend from a parent `Object` (in this case `Type`), and define any methods

The core library in ParaCode is written in itself, even allowing for methods to be attached with the `Object.patch()` method at runtime. Types in ParaCode are built of `Object`s and have overloadable functions for operations such as addition, subtraction, multiplication, division, modulus, and compare. Types including String, Int, Float, and Bool are all defined completely in ParaCode, including all operations that can be done on them. For instance, the call operator can be overloaded, with an example being that when a Number is called `5(10)` it multiplies the values together, allowing for a math-like syntax in programming.

ParaCode also has many methods that have functional language characteristics for example Array mapping and lambdas, and new concept ideas such as [Prototypical Inheritance](https://en.wikipedia.org/wiki/Prototype-based_programming). 

Later I plan to rewrite ParaCode in C/C++ for better speed, efficiency. I plan to keep ParaCode code and the standard library similar to how it is today.

[vars](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/00_vars.md) - How to declare and use variables

[functions](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/10_functions.md) - Writing and calling functions

[strings](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/15_strings.md) - Strings operations and interpolation

[operators](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/16_operators.md) - Available operators + Operator overloading

[types](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/20_types.md) - Custom types

[proto](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/30_proto.md) - Extending types using prototypical inheritance

[macros](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/35_macros.md) - Macros

[arrays](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/40_arrays.md) - Array operations

[iterators](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/50_iterators.md) - Building custom iterator objects

[random](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/55_random.md) - Random number generation

[modules](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/60_modules.md) - Modules

[console](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/70_console.md) - Console input and output

[files](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/80_files.md) - File reading and writing

[json](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#doc/81_json.md) - File reading and writing


### Examples

[embedding](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/embed.py)

[numbers](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/numbers.para)

[strings](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/string.para)

[patching](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/patching.para)

[operator overloading](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/operator_overloading.para)

[tic tac toe](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/ttt.para)

[pythagorean theorem calculator](https://repl.it/@DaRubyMiner360/ParaCode-Rewrite#examples/pythagorean.para)

Be sure to check out our TicTacToe example!
Start the REPL by running `main.py` and call `tictactoe();` to try it out!

To update ParaCode, run the `update.sh` file. On most operating systems this can be done with
```shell
sh update.sh
```
Or, to install and update ParaCode, run everything from `update.sh`.
