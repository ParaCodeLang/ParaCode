from interpreter.basic_value import BasicValue

def p(arguments):
    print(arguments.arguments[0].extract_value())
    return BasicValue(arguments.arguments[0].extract_value())

# Now just run:
# pyimport("examples/python_methods.py", "__p__", "p");
# To add it to ParaCode
