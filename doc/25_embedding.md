### Embedding

During the development of a program you may want
to use ParaCode code in Rust to interface between the
two languages. For this, we added a few important modules
in the `ParaCode` class to help interface with ParaCode.

The `ParaCode.callFunction` method takes in the name of the function
and a list containing arguments to be passed into the language.
`callFunction` returns the Rust value of the internal return
value in ParaCode. For example, calling `math.sqrtf` with arguments
`[25]` would result in a value of `5.0` stored in the respective type in Rust.

The `ParaCode.eval`, `ParaCode.evalData`, and `ParaCode.evalFile` methods
all take data passed in and evaluate them as ParaCode code. For example,
if we write `paraCode.evalData("print('Hello, %!'.format('World'));")`,
`evalData` would call ParaCode function `print`, call `str.format` on
`'Hello, %!'`, and output value to terminal.