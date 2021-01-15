### Embedding

During the development of a program you may want
to use ParaCode code in Python to interface between the
two languages. For this, we added a few important modules
in the `ParaCode` class to help interface with ParaCode.

The `ParaCode.call_function` method takes in the name of the function
and a list containing arguments to be passed into the language.
`call_function` returns the Python value of the internal return
value in ParaCode. For example, calling `math.sqrtf` with arguments
`[25]` would result in a value of `5.0` in Python.

The `ParaCode.eval`, `ParaCode.eval_data`, and `ParaCode.eval_file` methods
all take data passed in and evaluate them as ParaCode code. For example,
if we write `paracode.eval_data('print("Hello, %!".format("World"));')`,
`eval_data` would call ParaCode function `print`, call `str.format` on
`'Hello, %!'`, and output value to terminal.