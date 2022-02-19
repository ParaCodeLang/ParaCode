from interpreter.basic_value import BasicValue

# pyimport("examples/python_methods.py", "__testq__", "dictionaries");
# pyimport("examples/python_methods.py", "__testw__", "lists");

def dictionaries(arguments):
    return BasicValue({"A": "B"})

def lists(arguments):
    return BasicValue(["A", "B"])

def p(arguments):
    if len(arguments.arguments) > 0:
        print(arguments.arguments[0].extract_value())
        return BasicValue(arguments.arguments[0].extract_value())
    print("Nothing provided.")
    return BasicValue("Nothing provided.")

# Now just run:
# pyimport("examples/python_methods.py", "__p__", "p");
# pyimport("examples/python_methods.py", ["__p__"], ["p"]);
# pyimport("examples/python_methods.py", Dict.new(["__p__"], ["p"]));
# To add it to ParaCode
