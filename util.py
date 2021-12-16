class LogColor():
    Default = "\033[0m"
    Error = "\033[31;1m"
    Warning = "\033[33m"
    Info = "\033[34m"
    Bold = "\033[1m"

def fixiter(values, make_basic_value=True):
    from interpreter.basic_value import BasicValue

    result = []
    for value in values:
        if type(value) in [list, set, tuple]:
            result.append(fixiter(value))
        else:
            if make_basic_value:
                result.append(BasicValue(value))
            else:
                result.append(value)
    if make_basic_value:
        return BasicValue(result)
    else:
        return result
