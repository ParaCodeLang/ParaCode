class LogColor():
    Default = "\033[0m"
    Error = "\033[31;1m"
    Warning = "\033[33m"
    Info = "\033[34m"
    Bold = "\033[1m"

def fixiter(values, make_basic_value=True, skip_null=False):
    from interpreter.basic_value import BasicValue
    from interpreter.basic_object import BasicObject

    result = []
    for value in values:
        if type(value) in [list, set, tuple]:
            result.append(fixiter(value))
        else:
            if not isinstance(value, BasicValue) and make_basic_value:
                result.append(BasicValue(value))
            else:
                if isinstance(value, BasicObject):
                    if make_basic_value:
                        result.append(BasicValue(value.value))
                    else:
                        result.append(value.value)
                else:
                    result.append(value)
    if not isinstance(result, BasicValue) and make_basic_value:
        return BasicValue(result)
    else:
        if isinstance(value, BasicObject):
            if make_basic_value:
                return BasicValue(result.value)
            else:
                return result.value
        else:
            return result
