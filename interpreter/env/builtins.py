import os
import sys
import json

from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from interpreter.env.builtin.arith import *
from interpreter.env.builtin.time import *
from parse.node import NodeFunctionExpression, NodeCall, NodeArgumentList, NodeMemberExpression, NodeNone
from error import ErrorType
from util import LogColor

def obj_to_string(interpreter, node, obj):
    obj_str = str(obj)

    obj = interpreter.basic_value_to_object(node, obj)

    if isinstance(obj, BasicObject):
        meth = obj.lookup_member(BasicType.REPR_FUNCTION_NAME)

        basic_value_repr = None

        if meth is not None:
            if isinstance(meth.value, BuiltinFunction):
                basic_value_repr = interpreter.call_builtin_function(meth.value, obj, [], node)
            else:
                interpreter.stack.push(obj)
                interpreter.call_function_expression(meth.value)
                basic_value_repr = interpreter.stack.pop()

            if not isinstance(basic_value_repr, BasicValue):
                interpreter.error(node, ErrorType.TypeError, 'expected {} method to return an instance of BasicValue, got {}'.format(BasicType.REPR_FUNCTION_NAME, basic_value_repr))
                return None

            obj_str = basic_value_repr.value

    return obj_str

def _print_object(interpreter, node, obj, end='\n'):
    print(obj_to_string(interpreter, node, obj), end=end)
    
def builtin_varinfo(arguments):
    interpreter = arguments.interpreter
    var = interpreter.current_scope.find_variable_info(arguments.arguments[0].value)

    if var == None:
        return BasicValue("")

    varinfo_str = f"Variable '{arguments.arguments[0]}'\n\t" \
        f"decltype: {var.decltype}\n\t" \
        f"value: {var.value_wrapper}\n\t" \
        f"runtime type: {var.value_wrapper.lookup_type(interpreter.global_scope)}\n"
    

    return BasicValue(varinfo_str)

def builtin_run(arguments):
    interpreter = arguments.interpreter
    node = arguments.node

    for arg in arguments.arguments:
        _print_object(interpreter, node, arg)

    return BasicValue(len(arguments.arguments))

def builtin_console_write(arguments):
    interpreter = arguments.interpreter
    node = arguments.node

    for arg in arguments.arguments:
        _print_object(interpreter, node, arg, end='')

    return BasicValue(len(arguments.arguments))

def builtin_printn(arguments):
    interpreter = arguments.interpreter
    node = arguments.node

    for arg in arguments.arguments:
        _print_object(interpreter, node, arg)

    return BasicValue(len(arguments.arguments))

def builtin_print_color(arguments):
    color = arguments.arguments[0].extract_value()
    if color == 0:
        print(f"{LogColor.Default}", end="")
    elif color == 1:
        print(f"{LogColor.Error}", end="")
    elif color == 2:
        print(f"{LogColor.Warning}", end="")
    elif color == 3:
        print(f"{LogColor.Info}", end="")
    elif color == 4:
        print(f"{LogColor.Bold}", end="")
    return BasicValue(0)
    

def builtin_exit(arguments):
    interpreter = arguments.interpreter
    node        = arguments.node
    return_code = arguments.arguments[0]
    
    exit(return_code)
    
    return BasicValue(0)

def builtin_type_compare(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0]
    type_obj = arguments.arguments[1]

    if not isinstance(target, BasicObject):
        interpreter.error(node, ErrorType.TypeError, 'argument 1 ({}) is not a BasicObject, cannot perform typecheck'.format(target))
        return None

    if not isinstance(type_obj, BasicType):
        interpreter.error(node, ErrorType.TypeError, 'argument 2 ({}) is not a BasicType, cannot perform typecheck'.format(type_obj))

    if target.satisfies_type(type_obj):
        return BasicValue(1)
    else:
        return BasicValue(0)

# simple == compare
def builtin_default_compare(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0].extract_value()
    other = arguments.arguments[1].extract_value()

    return BasicValue(int(target == other))

def builtin_int_negate(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0].extract_value()

    return BasicValue(int(not target))

def builtin_to_int(arguments):
    return BasicValue(int(arguments.arguments[0].extract_value()))

def builtin_to_float(arguments):
    return BasicValue(float(arguments.arguments[0].extract_value()))

def builtin_str_len(arguments):
    return BasicValue(len(str(arguments.arguments[0].extract_value())))

def builtin_array_len(arguments):
    return BasicValue(len(arguments.arguments[0].extract_value()))

def builtin_dictionary_len(arguments):
    return BasicValue(len(arguments.arguments[0][0].extract_value()))

def builtin_array_set(arguments):
    array = arguments.arguments[0].extract_value()
    index = arguments.arguments[1].extract_value()
    value = arguments.arguments[2].extract_value()

    array[index] = value

    return BasicValue(array)

def builtin_dictionary_set(arguments):
    array = arguments.arguments[0][0].extract_value()
    index = arguments.arguments[0][1].extract_value()
    value = arguments.arguments[0][2].extract_value()

    array[index] = value

    return BasicValue(array)

def builtin_array_clone(arguments):
    array = arguments.arguments[0].extract_value()
    new_array = array.copy()
    return BasicValue(new_array)

def builtin_dictionary_clone(arguments):
    array = arguments.arguments[0][0].extract_value()
    new_array = array.copy()
    return BasicValue(new_array)

def builtin_array_at(arguments):
    obj = arguments.arguments[0].extract_value()
    index = arguments.arguments[1].extract_value()

    if index > len(obj):
        # TODO make throw internal exception
        return BasicValue(None)

    return BasicValue(obj[index])

def builtin_dictionary_at(arguments):
    obj = arguments.arguments[0][0].extract_value()
    index = arguments.arguments[0][1].extract_value()

    if index > len(obj):
        # TODO make throw internal exception
        return BasicValue(None)

    return BasicValue(obj[index])
    
def builtin_array_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    value_start = arguments.arguments[0]
    
    value = value_start.extract_value()

    if len(arguments.arguments) > 1:
        for arg in arguments.arguments[1:]:
            value.append(arg.extract_value())

    return BasicValue(value)


def builtin_dictionary_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    value_start = arguments.arguments[0][0]

    value = value_start.extract_value()

    if len(arguments.arguments[0]) > 1:
        for arg in arguments.arguments[0][1:]:
            value.append(arg.extract_value())

    return BasicValue(value)

def builtin_str_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    str_value_start = arguments.arguments[0]

    str_value = str(str_value_start.extract_value())

    if len(arguments.arguments) > 1:
        for arg in arguments.arguments[1:]:
            str_value = str_value + str(arg.extract_value())

    return BasicValue(str_value)

def builtin_str_replace(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    value = str(arguments.arguments[0].extract_value())
    toReplace = str(arguments.arguments[1].extract_value())
    replaceWith = str(arguments.arguments[2].extract_value())
		
    result = value
    
    if len(arguments.arguments) > 3:
      amount = int(str(arguments.arguments[3].extract_value()))
      result = value.replace(toReplace, replaceWith, amount)
    else:
      result = value.replace(toReplace, replaceWith)

    return BasicValue(result)

def builtin_str_tolower(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    value = str(arguments.arguments[0].extract_value())
    result = value.lower()
    
    return BasicValue(result)

def builtin_str_toupper(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    value = str(arguments.arguments[0].extract_value())
    result = value.upper()
    
    return BasicValue(result)

def builtin_eval(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    code = str(arguments.arguments[0].extract_value())
    codeGlobals = globals()
    codeLocals = locals()
    if len(arguments.arguments) > 1 and dict(arguments.arguments[1]) != []:
        codeGlobals = dict(arguments.arguments[1])
    if len(arguments.arguments) > 2 and dict(arguments.arguments[2]) != []:
        codeLocals = dict(arguments.arguments[2])
    result = exec(code, codeGlobals, codeLocals)
    codeGlobals.update(codeLocals)

    return BasicValue(result)

def builtin_object_new(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    new_instance = None

    if 'instance' in this_object.members and isinstance(this_object.members['instance'], BasicObject):
        new_instance = this_object.members['instance'].clone(parent_override=this_object)
    else:
        interpreter.error(None, ErrorType.TypeError, 'object {} cannot be constructed because no cloneable `instance` member exists'.format(this_object))
        return None

    # if there is a constructor function, call that...
    constructor_method_member = this_object.lookup_member('__construct__')

    if constructor_method_member is not None:
        constructor_method = constructor_method_member.value

        if isinstance(constructor_method, BuiltinFunction):
            interpreter.call_builtin_function(constructor_method, this_object, arguments.arguments, None)
        elif isinstance(constructor_method, NodeFunctionExpression):
            # push this object + any arguments passed here to the function
            passed_args = [new_instance, *arguments.arguments]

            for i in range(0, len(constructor_method.argument_list.arguments)):
                if i >= len(passed_args):
                    interpreter.stack.push(BasicValue(None))
                else:
                    interpreter.stack.push(passed_args[i])

            interpreter.call_function_expression(constructor_method)

            # pop return value off stack - if no `return X` is given,
            # a default value is pushed to stack anyway.
            interpreter.stack.pop()
        else:
            interpreter.error(None, ErrorType.TypeError, 'invalid constructor type {}'.format(constructor_method))

    return new_instance

def builtin_object_type(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if not isinstance(this_object, BasicValue):
        interpreter.error(None, ErrorType.TypeError, 'object {} is not an instance of BasicValue'.format(this_object))
        return None

    return this_object.lookup_type(interpreter.global_scope)

def builtin_object_is(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_objectaz
    target = arguments.arguments[0].extract_value()

    if not isinstance(this_object, BasicValue):
        interpreter.error(None, ErrorType.TypeError, 'object {} is not an instance of BasicValue'.format(this_object))
        return None

    return this_object.lookup_type(interpreter.global_scope) == target.lookup_type(interpreter.global_scope)

def builtin_object_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    return BasicValue('Object')

def builtin_object_patch(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    target = arguments.arguments[0].extract_value()
    patch = arguments.arguments[1].extract_value()

    if not isinstance(target, BasicObject):
        interpreter.error(this_object, ErrorType.TypeError, 'Cannot patch non-BasicObject value: {}'.format(target))
        return None

    if not isinstance(target, BasicObject):
        interpreter.error(this_object, ErrorType.TypeError, 'Cannot patch object with non-BasicObject value: {}'.format(patch))
        return None

    for (member_name, member_value) in patch.members.items():
        target.assign_member(member_name, member_value)

    return target

def builtin_value_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    passed_arg = arguments.arguments[0].extract_value()

    return BasicValue(str(passed_arg))

def builtin_num_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_str_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_type_extend(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if len(arguments.arguments) > 0:
        provided_args = arguments.arguments[0]

        if not isinstance(provided_args, BasicObject):
            interpreter.error('provided args to Type.extend must be an instance of BasicObject, got {}'.format(provided_args))
            return None

        extended_properties = provided_args.members
    else:
        extended_properties = {}

    instance_members = {}

    if 'instance' in this_object.members:
        instance_members = this_object.members['instance'].clone().members
        #for (member_name, member_value) in this_object.members['instance'].members.items():
         #instance_members[member_name] = member_value.clone()

    instance_members.update(extended_properties)

    return BasicType(this_object, instance_members)

def builtin_type_type(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if this_object.parent is not None:
        return this_object.parent

    return this_object.lookup_type(interpreter.global_scope)

def builtin_type_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    return BasicValue(repr(this_object))

def builtin_console_input(arguments):
    input_result = input()

    return BasicValue(input_result)

def builtin_file_read(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    # TODO better exception handling - throw internal exception
    try:
        f = open(file_path.extract_value(), 'r')
        s = f.read()
    except:
        s = ""

    return BasicValue(s)

def builtin_file_readlines(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    # TODO better exception handling - throw internal exception
    try:
        f = open(file_path.extract_value(), 'r')
        s = f.readlines()
    except:
        s = ""

    return BasicValue(s)

def builtin_file_write(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]
    write_value = arguments.arguments[1]

    f = open(file_path.extract_value(), 'w')
    f.write(str(write_value.extract_value()))
    f.close()

    return BasicValue(file_path)

def builtin_file_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]
    write_value = arguments.arguments[1]

    f = open(file_path.extract_value(), 'a')
    f.write(str(write_value.extract_value()))
    f.close()

    return BasicValue(file_path)

def builtin_file_create(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    f = open(file_path.extract_value(), 'x')
    f.close()

    return BasicValue(file_path)

def builtin_file_delete(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    os.remove(file_path.extract_value())

    return BasicValue(file_path)

def builtin_file_deletedir(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    os.rmdir(file_path.extract_value())

    return BasicValue(file_path)

def builtin_file_exists(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    return BasicValue(os.path.exists(file_path.extract_value()))

def builtin_is_file(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    return BasicValue(os.path.isfile(file_path.extract_value()))

def builtin_is_dir(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    return BasicValue(os.path.isdir(file_path.extract_value()))

def builtin_json_load(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    # TODO better exception handling - throw internal exception
    try:
        with open(file_path.extract_value(), "r") as f:
          s = json.load(f)
    except:
        s = json.loads("{\n}")

    return BasicValue(s)

def builtin_json_loads(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    text = arguments.arguments[0]

    # TODO better exception handling - throw internal exception
    try:
        s = json.loads(text.extract_value())
    except:
        s = json.loads("{\n}")

    return BasicValue(s)

def builtin_json_dump(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    data = arguments.arguments[0].extract_value()
    file = arguments.arguments[1].extract_value()
    doindent = False
    indent = -1
    if len(arguments.arguments) > 2:
        indent = arguments.arguments[2].extract_value()
        doindent = True

    with open(file, "w") as f:
        if doindent:
            json.dump(data, f, indent=indent)
        else:
            json.dump(data, f)
        return BasicValue(f.read())

    return BasicValue(None)

def builtin_json_dumps(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    data = arguments.arguments[0].extract_value()
    doindent = False
    indent = -1
    if len(arguments.arguments) > 1:
        indent = arguments.arguments[1].extract_value()
        doindent = True

    if doindent:
        return BasicValue(json.dumps(data, indent=indent))
    else:
        return BasicValue(json.dumps(data))

def builtin_numpara_mean(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    data = arguments.arguments[0].extract_value()
    for i in range(len(data)):
        if type(data[i]) == type(arguments.arguments[0]):
            data[i] = data[i].extract_value()

    import numpy
    
    result = numpy.mean(data)
    return BasicValue(result.item())

def builtin_numpara_median(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    data = arguments.arguments[0].extract_value()
    for i in range(len(data)):
        if type(data[i]) == type(arguments.arguments[0]):
            data[i] = data[i].extract_value()

    import numpy

    result = numpy.median(data)
    return BasicValue(result.item())

def builtin_scipara_mean(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    data = arguments.arguments[0].extract_value()
    for i in range(len(data)):
        if type(data[i]) == type(arguments.arguments[0]):
            data[i] = data[i].extract_value()

    import scipy
    
    result = scipy.mean(data)
    return BasicValue(result.item())

def builtin_scipara_median(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    data = arguments.arguments[0].extract_value()
    for i in range(len(data)):
        if type(data[i]) == type(arguments.arguments[0]):
            data[i] = data[i].extract_value()

    import scipy

    result = scipy.median(data)
    return BasicValue(result.item())

def builtin_scipara_mode(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    data = arguments.arguments[0].extract_value()
    for i in range(len(data)):
        if type(data[i]) == type(arguments.arguments[0]):
            data[i] = data[i].extract_value()

    from scipy import stats

    result = stats.mode(data)
    return BasicValue([result.mode, result.count])

def builtin_scipara_getliter(arguments):
    from scipy import constants

    liter = constants.liter
    return BasicValue(liter)

def builtin_scipara_getpi(arguments):
    from scipy import constants

    pi = constants.pi
    return BasicValue(pi)

def builtin_scipara_getyotta(arguments):
    from scipy import constants

    result = constants.yotta
    return BasicValue(result)

def builtin_scipara_getzetta(arguments):
    from scipy import constants

    result = constants.zetta
    return BasicValue(result)

def builtin_scipara_getexa(arguments):
    from scipy import constants

    result = constants.exa
    return BasicValue(result)

def builtin_scipara_getpeta(arguments):
    from scipy import constants

    result = constants.peta
    return BasicValue(result)

def builtin_scipara_gettera(arguments):
    from scipy import constants

    result = constants.tera
    return BasicValue(result)

def builtin_scipara_getgiga(arguments):
    from scipy import constants

    result = constants.giga
    return BasicValue(result)
    
def builtin_scipara_getmega(arguments):
    from scipy import constants

    result = constants.mega
    return BasicValue(result)

def builtin_scipara_getkilo(arguments):
    from scipy import constants

    result = constants.kilo
    return BasicValue(result)

def builtin_scipara_gethecto(arguments):
    from scipy import constants

    result = constants.hecto
    return BasicValue(result)

def builtin_scipara_getdeka(arguments):
    from scipy import constants

    result = constants.deka
    return BasicValue(result)

def builtin_scipara_getdeci(arguments):
    from scipy import constants

    result = constants.deci
    return BasicValue(result)

def builtin_scipara_getcenti(arguments):
    from scipy import constants

    result = constants.centi
    return BasicValue(result)

def builtin_scipara_getmilli(arguments):
    from scipy import constants

    result = constants.milli
    return BasicValue(result)

def builtin_scipara_getmicro(arguments):
    from scipy import constants

    result = constants.micro
    return BasicValue(result)

def builtin_scipara_getnano(arguments):
    from scipy import constants

    result = constants.nano
    return BasicValue(result)

def builtin_scipara_getpico(arguments):
    from scipy import constants

    result = constants.pico
    return BasicValue(result)

def builtin_scipara_getfemto(arguments):
    from scipy import constants

    result = constants.femto
    return BasicValue(result)

def builtin_scipara_getatto(arguments):
    from scipy import constants

    result = constants.atto
    return BasicValue(result)

def builtin_scipara_getzepto(arguments):
    from scipy import constants

    result = constants.zepto
    return BasicValue(result)

def builtin_scipara_getkibi(arguments):
    from scipy import constants

    result = constants.kibi
    return BasicValue(result)

def builtin_scipara_getmebi(arguments):
    from scipy import constants

    result = constants.mebi
    return BasicValue(result)

def builtin_scipara_getgibi(arguments):
    from scipy import constants

    result = constants.gibi
    return BasicValue(result)

def builtin_scipara_gettebi(arguments):
    from scipy import constants

    result = constants.tebi
    return BasicValue(result)

def builtin_scipara_getpebi(arguments):
    from scipy import constants

    result = constants.pebi
    return BasicValue(result)

def builtin_scipara_getexbi(arguments):
    from scipy import constants

    result = constants.exbi
    return BasicValue(result)

def builtin_scipara_getzebi(arguments):
    from scipy import constants

    result = constants.zebi
    return BasicValue(result)

def builtin_scipara_getyobi(arguments):
    from scipy import constants

    result = constants.yobi
    return BasicValue(result)

def builtin_scipara_getgram(arguments):
    from scipy import constants

    result = constants.gram
    return BasicValue(result)

def builtin_scipara_getmetric_ton(arguments):
    from scipy import constants

    result = constants.metric_ton
    return BasicValue(result)

def builtin_scipara_getgrain(arguments):
    from scipy import constants

    result = constants.grain
    return BasicValue(result)

def builtin_scipara_getlb(arguments):
    from scipy import constants

    result = constants.lb
    return BasicValue(result)

def builtin_scipara_getpound(arguments):
    from scipy import constants

    result = constants.pound
    return BasicValue(result)

def builtin_scipara_getoz(arguments):
    from scipy import constants

    result = constants.oz
    return BasicValue(result)

def builtin_scipara_getounce(arguments):
    from scipy import constants

    result = constants.ounce
    return BasicValue(result)

def builtin_scipara_getstone(arguments):
    from scipy import constants

    result = constants.stone
    return BasicValue(result)

def builtin_scipara_getlong_ton(arguments):
    from scipy import constants

    result = constants.long_ton
    return BasicValue(result)

def builtin_scipara_getshort_ton(arguments):
    from scipy import constants

    result = constants.short_ton
    return BasicValue(result)

def builtin_scipara_gettroy_ounce(arguments):
    from scipy import constants

    result = constants.troy_ounce
    return BasicValue(result)

def builtin_scipara_gettroy_pound(arguments):
    from scipy import constants

    result = constants.troy_pound
    return BasicValue(result)

def builtin_scipara_getcarat(arguments):
    from scipy import constants

    result = constants.carat
    return BasicValue(result)

def builtin_scipara_getatomic_mass(arguments):
    from scipy import constants

    result = constants.atomic_mass
    return BasicValue(result)

def builtin_scipara_getm_u(arguments):
    from scipy import constants

    result = constants.m_u
    return BasicValue(result)

def builtin_scipara_getu(arguments):
    from scipy import constants

    result = constants.u
    return BasicValue(result)

def builtin_scipara_getdegree(arguments):
    from scipy import constants

    result = constants.degree
    return BasicValue(result)

def builtin_scipara_getarcmin(arguments):
    from scipy import constants

    result = constants.arcmin
    return BasicValue(result)

def builtin_scipara_getarcminute(arguments):
    from scipy import constants

    result = constants.arcminute
    return BasicValue(result)

def builtin_scipara_getarcsec(arguments):
    from scipy import constants

    result = constants.arcsec
    return BasicValue(result)

def builtin_scipara_getarcsecond(arguments):
    from scipy import constants

    result = constants.arcsecond
    return BasicValue(result)

def builtin_scipara_getminute(arguments):
    from scipy import constants

    result = constants.minute
    return BasicValue(result)

def builtin_scipara_gethour(arguments):
    from scipy import constants

    result = constants.hour
    return BasicValue(result)

def builtin_scipara_getday(arguments):
    from scipy import constants

    result = constants.day
    return BasicValue(result)

def builtin_scipara_getweek(arguments):
    from scipy import constants

    result = constants.week
    return BasicValue(result)

def builtin_scipara_getyear(arguments):
    from scipy import constants

    result = constants.year
    return BasicValue(result)

def builtin_scipara_getJulian_year(arguments):
    from scipy import constants

    result = constants.Julian_year
    return BasicValue(result)

def builtin_scipara_getinch(arguments):
    from scipy import constants

    result = constants.inch
    return BasicValue(result)

def builtin_scipara_getfoot(arguments):
    from scipy import constants

    result = constants.foot
    return BasicValue(result)

def builtin_scipara_getyard(arguments):
    from scipy import constants

    result = constants.yard
    return BasicValue(result)

def builtin_scipara_getmile(arguments):
    from scipy import constants

    result = constants.mile
    return BasicValue(result)

def builtin_scipara_getmil(arguments):
    from scipy import constants

    result = constants.mil
    return BasicValue(result)

def builtin_scipara_getpt(arguments):
    from scipy import constants

    result = constants.pt
    return BasicValue(result)

def builtin_scipara_getpoint(arguments):
    from scipy import constants

    result = constants.point
    return BasicValue(result)

def builtin_scipara_getsurvey_foot(arguments):
    from scipy import constants

    result = constants.survey_foot
    return BasicValue(result)

def builtin_scipara_getsurvey_mile(arguments):
    from scipy import constants

    result = constants.survey_mile
    return BasicValue(result)

def builtin_scipara_getnautical_mile(arguments):
    from scipy import constants

    result = constants.nautical_mile
    return BasicValue(result)

def builtin_scipara_getfermi(arguments):
    from scipy import constants

    result = constants.fermi
    return BasicValue(result)

def builtin_scipara_getangstrom(arguments):
    from scipy import constants

    result = constants.angstrom
    return BasicValue(result)

def builtin_scipara_getmicron(arguments):
    from scipy import constants

    result = constants.micron
    return BasicValue(result)

def builtin_scipara_getau(arguments):
    from scipy import constants

    result = constants.au
    return BasicValue(result)

def builtin_scipara_getastronomical_unit(arguments):
    from scipy import constants

    result = constants.astronomical_unit
    return BasicValue(result)

def builtin_scipara_getlight_year(arguments):
    from scipy import constants

    result = constants.light_year
    return BasicValue(result)

def builtin_scipara_getparsec(arguments):
    from scipy import constants

    result = constants.parsec
    return BasicValue(result)

def builtin_scipara_getatm(arguments):
    from scipy import constants

    result = constants.atm
    return BasicValue(result)

def builtin_scipara_getatmosphere(arguments):
    from scipy import constants

    result = constants.atmosphere
    return BasicValue(result)

def builtin_scipara_getbar(arguments):
    from scipy import constants

    result = constants.bar
    return BasicValue(result)

def builtin_scipara_gettorr(arguments):
    from scipy import constants

    result = constants.torr
    return BasicValue(result)

def builtin_scipara_getmmHg(arguments):
    from scipy import constants

    result = constants.mmHg
    return BasicValue(result)

def builtin_scipara_getpsi(arguments):
    from scipy import constants

    result = constants.psi
    return BasicValue(result)

def builtin_scipara_getectare(arguments):
    from scipy import constants

    result = constants.ectare
    return BasicValue(result)

def builtin_scipara_getacre(arguments):
    from scipy import constants

    result = constants.acre
    return BasicValue(result)

def builtin_scipara_getliter(arguments):
    from scipy import constants

    result = constants.liter
    return BasicValue(result)

def builtin_scipara_getlitre(arguments):
    from scipy import constants

    result = constants.litre
    return BasicValue(result)

def builtin_scipara_getgallon(arguments):
    from scipy import constants

    result = constants.gallon
    return BasicValue(result)

def builtin_scipara_getgallon_US(arguments):
    from scipy import constants

    result = constants.gallon_US
    return BasicValue(result)

def builtin_scipara_getgallon_imp(arguments):
    from scipy import constants

    result = constants.gallon_imp
    return BasicValue(result)

def builtin_scipara_getfluid_ounce(arguments):
    from scipy import constants

    result = constants.fluid_ounce
    return BasicValue(result)

def builtin_scipara_getfluid_ounce_US(arguments):
    from scipy import constants

    result = constants.fluid_ounce_US
    return BasicValue(result)

def builtin_scipara_getfluid_ounce_imp(arguments):
    from scipy import constants

    result = constants.fluid_ounce_imp
    return BasicValue(result)

def builtin_scipara_getbarrel(arguments):
    from scipy import constants

    result = constants.barrel
    return BasicValue(result)

def builtin_scipara_getbbl(arguments):
    from scipy import constants

    result = constants.bbl
    return BasicValue(result)

def builtin_scipara_getkmh(arguments):
    from scipy import constants

    result = constants.kmh
    return BasicValue(result)

def builtin_scipara_getmph(arguments):
    from scipy import constants

    result = constants.mph
    return BasicValue(result)

def builtin_scipara_getmach(arguments):
    from scipy import constants

    result = constants.mach
    return BasicValue(result)

def builtin_scipara_getspeed_of_sound(arguments):
    from scipy import constants

    result = constants.speed_of_sound
    return BasicValue(result)

def builtin_scipara_getknot(arguments):
    from scipy import constants

    result = constants.knot
    return BasicValue(result)

def builtin_scipara_getzero_Celsius(arguments):
    from scipy import constants

    result = constants.zero_Celsius
    return BasicValue(result)

def builtin_scipara_getdegree_Fahrenheit(arguments):
    from scipy import constants

    result = constants.degree_Fahrenheit
    return BasicValue(result)

def builtin_scipara_geteV(arguments):
    from scipy import constants

    result = constants.eV
    return BasicValue(result)

def builtin_scipara_getelectron_volt(arguments):
    from scipy import constants

    result = constants.electron_volt
    return BasicValue(result)

def builtin_scipara_getcalorie(arguments):
    from scipy import constants

    result = constants.calorie
    return BasicValue(result)

def builtin_scipara_getcalorie_th(arguments):
    from scipy import constants

    result = constants.calorie_th
    return BasicValue(result)

def builtin_scipara_getcalorie_IT(arguments):
    from scipy import constants

    result = constants.calorie_IT
    return BasicValue(result)

def builtin_scipara_geterg(arguments):
    from scipy import constants

    result = constants.erg
    return BasicValue(result)

def builtin_scipara_getBtu(arguments):
    from scipy import constants

    result = constants.Btu
    return BasicValue(result)

def builtin_scipara_getBtu_IT(arguments):
    from scipy import constants

    result = constants.Btu_IT
    return BasicValue(result)

def builtin_scipara_getBtu_th(arguments):
    from scipy import constants

    result = constants.Btu_th
    return BasicValue(result)

def builtin_scipara_getton_TNT(arguments):
    from scipy import constants

    result = constants.ton_TNT
    return BasicValue(result)

def builtin_scipara_gethp(arguments):
    from scipy import constants

    result = constants.hp
    return BasicValue(result)

def builtin_scipara_gethorsepower(arguments):
    from scipy import constants

    result = constants.horsepower
    return BasicValue(result)

def builtin_scipara_getdyn(arguments):
    from scipy import constants

    result = constants.dyn
    return BasicValue(result)

def builtin_scipara_getdyne(arguments):
    from scipy import constants

    result = constants.dyne
    return BasicValue(result)

def builtin_scipara_getlbf(arguments):
    from scipy import constants

    result = constants.lbf
    return BasicValue(result)

def builtin_scipara_getpound_force(arguments):
    from scipy import constants

    result = constants.pound_force
    return BasicValue(result)

def builtin_scipara_getkgf(arguments):
    from scipy import constants

    result = constants.kgf
    return BasicValue(result)

def builtin_scipara_getkilogram_force(arguments):
    from scipy import constants

    result = constants.kilogram_force
    return BasicValue(result)

def builtin_scipara_getversion(arguments):
    import scipy

    version = scipy.__version__
    return BasicValue(version)

def builtin_os_args(arguments):
    return BasicValue(sys.argv)

def builtin_clear(arguments):
    # Windows
    if os.name == 'nt':
      os.system('cls')
    
    # Mac and Linux
    else:
      os.system('clear')

    return BasicValue(None)

def builtin_quit(arguments):
    if len(arguments.arguments) > 0:
      quit(int(str(arguments.arguments[0])))
    else:
      quit()

    return BasicValue(None)

def builtin_sysexit(arguments):
    if len(arguments.arguments) > 0:
      sys.exit(str(arguments.arguments[0]))
    else:
      sys.exit()

    return BasicValue(None)

def builtin_func_call(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    meth = arguments.arguments[0]
    arg_array = arguments.arguments[1].extract_value()

    if not isinstance(arg_array, list):
        interpreter.error(node, ErrorType.TypeError, '__intern_func_call__ expects arguments to be passed as an array but got {}'.format(arg_array))
        return None

    if isinstance(meth, BuiltinFunction):
        basic_value_resp = interpreter.call_builtin_function(meth, this_object, arg_array, node)
    else:
        for arg in arg_array:
            interpreter.stack.push(arg)
        interpreter.call_function_expression(meth)
        basic_value_resp = interpreter.stack.pop()

    return basic_value_resp

def builtin_math_max(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    values = []

    for arg in arguments.arguments:
        v = arg.extract_value()
        values.append(v)

    max_value = max(values)

    return BasicValue(max_value)

def builtin_math_min(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    values = []

    for arg in arguments.arguments:
        v = arg.extract_value()
        values.append(v)

    min_value = min(values)

    return BasicValue(min_value)

def builtin_macro_expand(arguments):
    from lexer import Lexer
    from parse.parser import Parser

    interpreter = arguments.interpreter
    this_object = arguments.this_object
    src_data = arguments.arguments[0].extract_value()

    if not isinstance(src_data, str):
        interpreter.error(arguments.node, ErrorType.TypeError, 'Expected a string for macro expansion')
        return None

    lexer = Lexer(src_data, interpreter.source_location)
    tokens = lexer.lex()

    parser = Parser(tokens, lexer.source_location)
    
    ast = parser.parse()

    if len(parser.error_list.errors) > 0:
        interpreter.error(arguments.node, ErrorType.MacroExpansionError, 'Macro expansion failed:\n{}'.format('\t'.join(map(lambda x: str(x), parser.error_list.errors))))
        return None

    for node in ast:
        interpreter.visit(node)

    return BasicValue(None)
