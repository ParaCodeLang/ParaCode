from interpreter.basic_value import BasicValue

def p(arguments):
    if len(arguments.arguments) > 0:
        print(arguments.arguments[0].extract_value())
        return BasicValue(arguments.arguments[0].extract_value())
    print("Nothing provided.")
    return BasicValue("Nothing provided.")

# Now just run:
# pyimport("examples/python_methods.py", ["p": "__p__"]);
# To add it to ParaCode.
# The first parameter is the python file's path
# The second parameter is a dictionary where the keys
# are the python function names and the values are the
# ParaCode function names.
