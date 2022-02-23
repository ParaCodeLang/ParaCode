from parse.parser import Parser
from parse.node import AstNode, NodeType, NodeFunctionReturn
from parse.source_location import SourceLocation
from parse.node import *

from interpreter.scope import *
from interpreter.stack import Stack
from interpreter.function import BuiltinFunction, BuiltinFunctionArguments
from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.env.globals import Globals
from interpreter.variable import VariableType
from interpreter.env.builtins import builtin_object_new, obj_to_string
from lexer import TokenType, LexerToken

from error import InterpreterError, ErrorList, ErrorType, Error

class ReturnJump(Exception):
    pass

class Interpreter():
    def __init__(self, source_location):
        self.source_location = source_location
        self.error_list = ErrorList()
        # declare scopes + global scope
        self.stack = Stack()

        self.in_try = False
        
        self.global_scope = Scope(None)
        self._top_level_scope = None

        # _globals is only used for pyimport
        self._globals = Globals()
        self._globals.apply_to_scope(self.global_scope)

    @property
    def current_scope(self):
        if self._top_level_scope is not None:
            return self._top_level_scope

        return self.global_scope

    def open_scope(self):
        self._top_level_scope = Scope(self.current_scope)

    def close_scope(self):
        if self.current_scope == self.global_scope:
            raise Exception('cannot close global scope!')
        self._top_level_scope = self.current_scope.parent

        return self.current_scope

    def error(self, node, type, message, cont=False, name=None, classnames=None, object=None):
        if name is None and classnames is None:
            if type == ErrorType.Syntax:
                name = "Syntax Error"
                classnames = ["Exception", "SyntaxError"]
            elif type == ErrorType.DoesNotExist:
                name = "DoesNotExist Error"
                classnames = ["Exception", "DoesNotExistError"]
            elif type == ErrorType.TypeError:
                name = "Type Error"
                classnames = ["Exception", "TypeError"]
            elif type == ErrorType.MultipleDefinition:
                name = "Multiple Definition Error"
                classnames = ["Exception", "MultipleDefinitionError"]
            elif type == ErrorType.ArgumentError:
                name = "Argument Error"
                classnames = ["Exception", "Argument Error"]
            elif type == ErrorType.InterruptedError:
                name = "Interrupted Error"
                classnames = ["Exception", "InterruptedError"]
            elif type == ErrorType.MacroExpansionError:
                name = "Macro Expansion Error"
                classnames = ["Exception", "MacroExpansionError"]
            else:
                name = "Exception"
                classnames = ["Exception"]

        location = None

        if node is not None:
            location = node.location

        if not cont and self.in_try:
            raise InterpreterError('Interpreter error', node, type, message, cont, name, classnames, object)

        err = Error(type, location, message, self.source_location.filename, name)
        self.error_list.push_error(err)
        self.error_list.print_errors()

        if cont or not self.in_try:
            raise InterpreterError('Interpreter error', node, type, message, cont, name, classnames, object)
        
    def visit(self, node, allow_casting=False):
        if isinstance(node, BasicValue):
            return node

        try:
            caller_name = "visit_{}".format(str(node.type.name))
            caller = getattr(self, caller_name)
        except:
            raise Exception('No visitor function defined for node {}'.format(node))

        if caller_name == "visit_Assign":
            return caller(node, allow_casting)
        return caller(node)

    def visit_UnaryOp(self, node):
        funstr = '__noop__'
        
        if node.token.type == TokenType.Plus:
            val = self.visit(node.expression)
            return BasicValue(+val.value)
        elif node.token.type == TokenType.Minus:
            val = self.visit(node.expression)
            return BasicValue(-val.value)
            
        elif node.token.type == TokenType.Not:
            funstr = '__not__'
            # if val is None or val.value == 0:
            #     return BasicValue(1)
            # else:
            #     return BasicValue(0)

        elif node.token.type == TokenType.BitwiseNot:
            funstr = '__bitnot__'

        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.expression,
                LexerToken(funstr, TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [],
                node.token
            )
        )

        return self.visit(member_access_call_node)
            
    def visit_BinOp(self, node):
        funstr = '__noop__'
        
        if node.token.type == TokenType.Plus:
            funstr = '__add__'
        elif node.token.type == TokenType.Minus:
            funstr = '__sub__'
        elif node.token.type == TokenType.Multiply:
            funstr = '__mul__'
        elif node.token.type == TokenType.Exponentiation:
            funstr = '__expon__'
        elif node.token.type == TokenType.Divide:
            funstr = '__div__'
        elif node.token.type == TokenType.Modulus:
            funstr = '__mod__'
        elif node.token.type == TokenType.LessThan:
            funstr = '__lt__'
        elif node.token.type == TokenType.LessThanEqual:
            funstr = '__lte__'
        elif node.token.type == TokenType.GreaterThan:
            funstr = '__gt__'
        elif node.token.type == TokenType.GreaterThanEqual:
            funstr = '__gte__'
        elif node.token.type == TokenType.Compare:
            funstr = '__eql__'
        elif node.token.type == TokenType.NotCompare:
            funstr = '__noteql__'
        elif node.token.type == TokenType.And:
            funstr = '__and__'
        elif node.token.type == TokenType.Or:
            funstr = '__or__'
        elif node.token.type == TokenType.BitwiseOr:
            funstr = '__bitor__'
        elif node.token.type == TokenType.BitwiseAnd:
            funstr = '__bitand__'
        elif node.token.type == TokenType.BitwiseXor:
            funstr = '__bitxor__'
        elif node.token.type == TokenType.BitwiseLShift:
            funstr = '__bitshiftleft__'
        elif node.token.type == TokenType.BitwiseRShift:
            funstr = '__bitshiftright__'
        elif node.token.type == TokenType.Spaceship:
            funstr = '__compare__'
            
        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.left,
                LexerToken(funstr, TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [node.right],
                node.token
            )
        )
        return self.visit(member_access_call_node)
        
    def visit_Type(self, node):
        pass
    
    def visit_Declare(self, node):
        type_node_value = None

        if isinstance(node, NodeSplatArgument):
            node = NodeDeclare(None, node.token, NodeNone(node.token))
        if node.type_node is not None:
            type_node_value = self.visit(node.type_node)

        if self.current_scope.find_variable_info(node.name.value, limit=True) != None:
            self.error(node, ErrorType.MultipleDefinition, "multiple definition of '{}'".format(node.name.value))
   
        self.current_scope.declare_variable(node.name.value, type_node_value, node.allow_casting)
        val = self.visit(node.value, node.allow_casting)
        return val
    
    def visit_Import(self, node):
        # the imported file is already lexed and parsed from the parser, so this
        # acts like a block and visits the statements inside. This means that if we
        # import inside a function, any variables should only be available to that
        # scope.
        old_source_location = self.source_location
        self.source_location = node.source_location

        for child in node.children:
            self.visit(child)

        self.source_location = old_source_location
    
    def visit_FunctionReturn(self, node):
        value = self.visit(node.value_node)
        self.stack.push(value)
        raise ReturnJump()
    
    def visit_Number(self, node):
        return BasicValue(node.value)
    
    def visit_String(self, node):
        return BasicValue(node.value)
            
    def visit_Block(self, node, create_scope=True):
        if create_scope:
            self.open_scope()
        
        # visit each statement in block
        for child in node.children:
            self.visit(child)
            
        if create_scope:
            self.close_scope()

    def assignment_typecheck(self, node, type_object, assignment_value, detailed_return=False, allow_casting=False):
        if type_object is None:
            self.error(node, ErrorType.TypeError, 'Set with decltype but decltype resolved to None')
            if detailed_return:
                return False, assignment_value
            return False
        elif not isinstance(type_object, BasicType):
            self.error(node, ErrorType.TypeError, '{} is not a valid type object and cannot be used as a declaration type'.format(type_object))
            if detailed_return:
                return False, assignment_value
            return False
        else:
            assignment_type = BasicValue(assignment_value).lookup_type(self.global_scope)

            if isinstance(assignment_type, BasicObject):
                assignment_type = assignment_value.parent

            if assignment_type is None:
                self.error(node, ErrorType.TypeError, 'Assignment requires type {} but could not resolve a runtime type of assignment value'.format(type_object))
                if detailed_return:
                    return None, assignment_value
                return None
            if isinstance(assignment_type, BasicValue):
                assignment_type = assignment_type.extract_value()

            if not isinstance(assignment_type, BasicType):
                self.error(node, ErrorType.TypeError, '{} is not a valid runtime type object'.format(assignment_type))
                if detailed_return:
                    return False, assignment_value
                return False
    
            if not type_object.compare_type(assignment_type):
                if allow_casting:
                    try:
                        assignment_value = builtin_object_new(BuiltinFunctionArguments(interpreter=self, this_object=type_object, arguments=[assignment_value], node=node))
                        assignment_type = type_object
                    except:
                        self.error(node, ErrorType.TypeError, 'Attempted to assign <{}> to a value of type <{}>'.format(type_object.friendly_typename, assignment_type.friendly_typename))
                        if detailed_return:
                            return False, assignment_value
                        return False
                else:
                    self.error(node, ErrorType.TypeError, 'Attempted to assign <{}> to a value of type <{}>'.format(type_object.friendly_typename, assignment_type.friendly_typename))
                    if detailed_return:
                        return False, assignment_value
                    return False

        if detailed_return:
            return True, assignment_value
        return True

    def visit_Assign(self, node, allow_casting=False):
        if isinstance(node.lhs, NodeVariable):
            node.allow_casting = allow_casting
            target_info = self.walk_variable(node.lhs)
            target_value = target_info.value_wrapper

            value = self.visit(node.value)
            # TYPE CHECK
            if target_info.decltype is not None:
                typecheck_value, value = self.assignment_typecheck(node.lhs, target_info.decltype, value, True, allow_casting)

                if typecheck_value is not True:
                    return None

            target_value.assign_value(value)
            return value

        elif isinstance(node.lhs, NodeMemberExpression):
            (target, member) = self.walk_member_expression(node.lhs)

            if not isinstance(target, BasicObject):
                self.error(node, ErrorType.TypeError, 'member expression not assignable')
                return None

            target_type = target.parent

            value = self.visit(node.value)
            target.assign_member(member.name, value)
            return value
        elif isinstance(node.lhs, NodeArrayAccessExpression):
            member_access_call_node = NodeCall(
                NodeMemberExpression(
                    node.lhs.lhs,
                    LexerToken('__set__', TokenType.Identifier),
                    node.lhs.token
                ),
                NodeArgumentList(
                    [node.lhs.access_expr, node.value],

                    node.lhs.token
                )
            )

            return self.visit(member_access_call_node)

        else:
            self.error(node, ErrorType.TypeError, 'cannot assign {}'.format(node.lhs))

            return None
            
    def collect_args(self, node):
        collected_args = []
        for arg in node.argument_list.arguments:
            arg_visited = self.visit(arg)

            if type(arg_visited) == list:
                for arg in arg_visited:
                    collected_args.append(arg)
            else:
                collected_args.append(arg_visited)

        return collected_args

    def wrap_arg_in_node(self, name, arg):
        if type(arg) == str:
            return NodeString(LexerToken('"{}"'.format(arg)))
        elif type(arg) in (float, int):
            return NodeNumber(LexerToken(str(arg)))
        elif type(arg) == list:
            return NodeArrayExpression(
                map(lambda x: self.wrap_arg_in_node(name, x), arg),
                LexerToken(name, TokenType.Identifier)
            )
        else:
            raise Exception("Invalid argument {} type({}) not supported".format(arg, type(arg)))

    def call_function(self, name, args):
        from ParaCode import ParaCode

        retval = 0
        node_args = []
        for arg in args:
            node_args.append(self.wrap_arg_in_node(name, arg))

        paraCode = ParaCode()
        paraCode.eval(data="{};".format(name), interpret=False, default_imports=[])
        lhs = paraCode.ast[0]
        name_token = LexerToken(name, TokenType.Identifier)
        

        if isinstance(lhs, NodeMemberExpression):
            parent, member = self.walk_member_expression(lhs)
            target = member.value
            node_args = [parent]+node_args
        else:
            target = lhs

        call_node = NodeCall(
            target,
            NodeArgumentList(
                node_args,
                name_token
            )
        )
        return self.visit_Call(call_node).extract_value()
    
    def visit_Call(self, node):
        this_arg = None
        is_member_call = False

        target = None

        # for `a.b()`, pass in `a` as the this value.
        if isinstance(node.lhs, NodeMemberExpression):
            t, m = self.walk_member_expression(node.lhs)
            target = m.value
            this_arg = t

            is_member_call = True
        else:
            target = self.visit(node.lhs)
        return_value = 0
        
        if target is not None:
            if isinstance(target, BuiltinFunction):
                collected_args = self.collect_args(node)
                
                this_value = None
                
                if this_arg is not None:
                    this_value = this_arg
                
                return self.call_builtin_function(target, this_value, collected_args, node)
            # user-defined function
            elif isinstance(target, NodeFunctionExpression):
                collected_args = self.collect_args(node)
                if is_member_call: # a.b('test') -> pass 'a' in as first argument
                    if this_arg is not None:
                        this_value = this_arg
                        if this_value is not None:
                            collected_args = [this_value, *collected_args]

                expected_arg_count = len(target.argument_list.arguments)
                given_arg_count = len(collected_args)
                original_given_arg_count = given_arg_count

                if isinstance(target.argument_list.arguments[-1], NodeSplatArgument):
                    if given_arg_count > 0:
                        new_collected_args = []
                        for i in range(0, given_arg_count):
                            if i < expected_arg_count - 1:
                                new_collected_args.append(collected_args[i])
                            elif i == expected_arg_count - 1:
                                new_collected_args.append([])
                                try:
                                    value = BasicValue(eval(collected_args[i]))
                                except:
                                    value = BasicValue(eval(str(BasicType(collected_args[i]))))
                                new_collected_args[expected_arg_count - 1].append(value)
                            elif i > expected_arg_count - 1:
                                try:
                                    value = BasicValue(eval(collected_args[i]))
                                except:
                                    value = BasicValue(eval(str(BasicType(collected_args[i]))))
                                new_collected_args[expected_arg_count - 1].append(value)
                        amount = len(new_collected_args)
                        for i in range(0, expected_arg_count):
                            if i > amount - 1:
                                new_collected_args.append([])
                        collected_args = new_collected_args
                        if not isinstance(collected_args[-1], BasicObject) and not isinstance(collected_args[-1], BasicValue) and not isinstance(collected_args[-1], BasicType):
                            try:
                                value = BasicValue(eval(collected_args[-1]))
                            except:
                                value = BasicValue(eval(str(BasicType(collected_args[-1]))))
                        else:
                            value = collected_args[-1]
                        collected_args[-1] = value
                        given_arg_count = len(collected_args)
                    else:
                        collected_args.append(BasicValue([]))
                        given_arg_count = len(collected_args)
                elif expected_arg_count < given_arg_count:
                    self.error(node, ErrorType.ArgumentError, 'method expected {} arguments, {} given'.format(expected_arg_count, original_given_arg_count))
                    return None
                for i in range(0, expected_arg_count):
                    if i >= given_arg_count:
                        if isinstance(target.argument_list.arguments[i], NodeSplatArgument):
                            arg = NodeDeclare(None, target.argument_list.arguments[i].token, NodeNone(target.argument_list.arguments[i].token))
                        else:
                            arg = target.argument_list.arguments[i]
                        if not isinstance(arg.value, NodeNone):
                            try:
                                value = BasicValue(eval(target.argument_list.arguments[i].value.value.token.value))
                            except:
                                value = BasicValue(eval(str(BasicType(target.argument_list.arguments[i].value.value.token.value))))
                            collected_args.append(value)
                            given_arg_count += 1
                if expected_arg_count > given_arg_count:
                    self.error(node, ErrorType.ArgumentError, 'method expected {} arguments, {} given'.format(expected_arg_count, given_arg_count))
                    return None

                # typecheck args
                for i in range(0, expected_arg_count):
                    if isinstance(target.argument_list.arguments[i], NodeSplatArgument):
                        target_arg = NodeDeclare(None, target.argument_list.arguments[i].token, NodeNone(target.argument_list.arguments[i].token))
                    else:
                        target_arg = target.argument_list.arguments[i]
                    call_arg = collected_args[i]

                    type_node = target_arg.type_node

                    if type_node is not None:
                        decltype = self.visit(type_node)
                        
                        self.assignment_typecheck(target_arg, decltype, call_arg)

                # push arguments to stack
                for arg in collected_args:
                    self.stack.push(arg)
                
                self.call_function_expression(target)
                # the return value is pushed onto the stack at end of block or return
                # statement. Pop it off and return as a value

                result = self.stack.pop()

                if not isinstance(result, BasicValue):
                    self.error(node, ErrorType.TypeError, 'expected method to return an instance of BasicValue, got {}'.format(result))
                    return None

                return result
            else: # objects......
                if this_arg is None:
                    this_arg = NodeNone(node.token)

                member_access_call_node = NodeCall(
                    NodeMemberExpression(
                        target,
                        LexerToken('__call__', TokenType.Identifier),
                        node.token
                    ),
                    NodeArgumentList(
                        [
                            NodeArrayExpression(
                                [this_arg]+node.argument_list.arguments,
                                node.token
                            )
                        ],
                        node.token
                    )
                )
                return self.visit(member_access_call_node)

        self.error(node, ErrorType.TypeError, 'invalid call: {} is not callable'.format(target))

    def walk_variable(self, node):
        var = self.current_scope.find_variable_info(node.value)
        if var is None:
            self.error(node, ErrorType.DoesNotExist, "Referencing undefined variable '{}'".format(node.value))
            return None

        return var
            
    def visit_Variable(self, node):
        var = self.walk_variable(node)

        if var is not None:
            return var.value_wrapper.value

        return None

    def check_object_truthy(self, node):
        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node,
                LexerToken('__bool__', TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [],
                node.token
            )
        )

        result = self.visit(member_access_call_node)

        if result is None:
            self.error(node, ErrorType.TypeError, 'cannot check if object {} is truthy'.format(node))
            return None

        int_result = result.extract_value()

        if type(int_result) != int:
            self.error(node, ErrorType.TypeError, 'expected __bool__ call to return an int'.format(node))
            return None

        return int_result != 0

    def visit_IfStatement(self, node):
        truthy_result = self.check_object_truthy(node.expr)

        if truthy_result:
            return self.visit_Block(node.block)
        elif node.else_block is not None:
            # use visit rather than direct to visit_Block
            # since else_block can also be a NodeIfStatement in the
            # case of `elif`
            return self.visit(node.else_block)

    def visit_Try(self, node):
        if node.catch_block is not None and node.catch_block != [] and node.else_block is None and node.finally_block is None:
            print("AA")
            try:
                self.in_try = True
                return self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                found = False
                for i in range(len(node.catch_block)):
                    if node.expr[i] is None:
                        if i == len(node.catch_block) - 1:
                            self.in_try = True
                            return self.visit_Block(node.catch_block[i])
                        else:
                            found = True
                            self.visit_Block(node.catch_block[i])
                    else:
                        if type(node.expr[i]) == list:
                            for value in node.expr[i]:
                                if value.token.value in e.classnames:
                                    if i == len(node.catch_block) - 1:
                                        self.in_try = True
                                        return self.visit_Block(node.catch_block[i])
                                    else:
                                        found = True
                                        self.visit_Block(node.catch_block[i])
                        elif type(node.expr[i].token.value) == str:
                            print("AAA")
                            # print(node.expr[i].token.value)
                            # print(e.object.members["message"])
                            # print(node.expr[i + 1].token.value)
                            if node.expr[i].token.value in e.classnames:
                                if node.variable[i] is not None:
                                    node.variable[i].type_node.token.value = node.expr[i].token.value
                                    # print(node.variable[i].value)
                                    # node.variable[i].value.token.token.value = e.object
                                    # print(node.variable[i].value)
                                    self.visit_Declare(node.variable[i])
                                    
                                if i == len(node.catch_block) - 1:
                                    self.in_try = True
                                    return self.visit_Block(node.catch_block[i])
                                else:
                                    found = True
                                    self.visit_Block(node.catch_block[i])
                            elif i == len(node.catch_block) - 1 and not found:
                                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                        elif i == len(node.catch_block) - 1 and not found:
                            self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
        elif node.catch_block is not None and node.catch_block != [] and node.else_block is None and node.finally_block is not None:
            print("B")
            try:
                self.in_try = True
                self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                found = False
                for i in range(len(node.catch_block)):
                    if node.expr[i] is None:
                        if i == len(node.catch_block) - 1:
                            self.in_try = True
                            return self.visit_Block(node.catch_block[i])
                        else:
                            found = True
                            self.visit_Block(node.catch_block[i])
                    else:
                        if type(node.expr[i]) == list:
                            for value in node.expr[i]:
                                if value.token.value in e.classnames:
                                    if i == len(node.catch_block) - 1:
                                        self.in_try = True
                                        return self.visit_Block(node.catch_block[i])
                                    else:
                                        found = True
                                        self.visit_Block(node.catch_block[i])
                        elif type(node.expr[i].token.value) == str:
                            if node.expr[i].token.value in e.classnames:
                                if i == len(node.catch_block) - 1:
                                    self.in_try = True
                                    return self.visit_Block(node.catch_block[i])
                                else:
                                    found = True
                                    self.visit_Block(node.catch_block[i])
                            elif i == len(node.catch_block) - 1 and not found:
                                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                        elif i == len(node.catch_block) - 1 and not found:
                            self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            finally:
                self.in_try = True
                return self.visit_Block(node.finally_block)
        elif (node.catch_block is not None and node.catch_block != []) and node.else_block is not None and node.finally_block is None:
            print("C")
            try:
                self.in_try = True
                self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                found = False
                for i in range(len(node.catch_block)):
                    if node.expr[i] is None:
                        if i == len(node.catch_block) - 1:
                            self.in_try = True
                            return self.visit_Block(node.catch_block[i])
                        else:
                            found = True
                            self.visit_Block(node.catch_block[i])
                    else:
                        if type(node.expr[i]) == list:
                            for value in node.expr[i]:
                                if value.token.value in e.classnames:
                                    if i == len(node.catch_block) - 1:
                                        self.in_try = True
                                        return self.visit_Block(node.catch_block[i])
                                    else:
                                        found = True
                                        self.visit_Block(node.catch_block[i])
                        elif type(node.expr[i].token.value) == str:
                            if node.expr[i].token.value in e.classnames:
                                if i == len(node.catch_block) - 1:
                                    self.in_try = True
                                    return self.visit_Block(node.catch_block[i])
                                else:
                                    found = True
                                    self.visit_Block(node.catch_block[i])
                            elif i == len(node.catch_block) - 1 and not found:
                                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                        elif i == len(node.catch_block) - 1 and not found:
                            self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            else:
                self.in_try = True
                return self.visit_Block(node.else_block)
        elif (node.catch_block is not None and node.catch_block != []) and node.else_block is not None and node.finally_block is not None:
            # BasicObject(parent=None, members={'raise': AstNode[FunctionExpression, AstNode[Block, LexerToken[Type:TokenType.Keyword, Value:'return']]], 'message': 'A'})
            try:
                self.in_try = True
                self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                found = False
                for i in range(len(node.catch_block)):
                    if node.expr[i] is None:
                        print("AB")
                        if i == len(node.catch_block) - 1:
                            self.in_try = True
                            return self.visit_Block(node.catch_block[i])
                        else:
                            found = True
                            self.visit_Block(node.catch_block[i])
                    else:
                        if type(node.expr[i]) == list:
                            print("B")
                            for value in node.expr[i]:
                                if value.token.value in e.classnames:
                                    if i == len(node.catch_block) - 1:
                                        self.in_try = True
                                        return self.visit_Block(node.catch_block[i])
                                    else:
                                        found = True
                                        self.visit_Block(node.catch_block[i])
                        elif type(node.expr[i].token.value) == str:
                            print("C")
                            if node.expr[i].token.value in e.classnames:
                                print("CA")
                                if i == len(node.catch_block) - 1:
                                    print("CAA")
                                    self.in_try = True
                                    return self.visit_Block(node.catch_block[i])
                                else:
                                    print("CAB")
                                    # print(node)
                                    found = True
                                    self.visit_Block(node.catch_block[i])
                            elif i == len(node.catch_block) - 1 and not found:
                                print("CB")
                                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                        elif i == len(node.catch_block) - 1 and not found:
                            print("D")
                            self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            else:
                self.visit_Block(node.else_block)
            finally:
                self.in_try = True
                return self.visit_Block(node.finally_block)
        elif (node.catch_block is None or node.catch_block == []) and node.else_block is not None and node.finally_block is None:
            print("E")
            try:
                self.in_try = True
                return self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            else:
                self.in_try = True
                return self.visit_Block(node.else_block)
        elif (node.catch_block is None or node.catch_block == []) and node.else_block is None and node.finally_block is not None:
            print("F")
            try:
                self.in_try = True
                return self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            finally:
                self.in_try = True
                return self.visit_Block(node.else_block)
        elif (node.catch_block is None or node.catch_block == []) and node.else_block is not None and node.finally_block is not None:
            try:
                self.in_try = True
                return self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            else:
                self.in_try = True
                return self.visit_Block(node.else_block)
            finally:
                self.in_try = True
                return self.visit_Block(node.finally_block)
        else:
            try:
                self.in_try = True
                return self.visit_Block(node.block)
            except InterpreterError as e:
                if e.type == ErrorType.Syntax:
                    self.in_try = False
                    return self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
                self.in_try = True
                self.error(e.node, e.type, e.message, True, e.name, e.classnames, e.object)
            
    def visit_While(self, node):
        truthy_result = self.check_object_truthy(node.expr)

        while truthy_result:
            self.visit_Block(node.block)

            truthy_result = self.check_object_truthy(node.expr)

    def visit_For(self, node):
        # call __iterate__ passing in a function expression
        # as a callback for each item in the iterable.

        # create an argument list with a single argument, the target.
        # it will be named whatever the var is in the for loop statement
        argument_list = NodeArgumentList(
            [NodeDeclare(None, node.var_token, NodeNone(node.token))],
            node.token
        )
        
        fnexpr_node = NodeFunctionExpression(argument_list, node.block)

        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.expr,
                LexerToken('__iterate__', TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [fnexpr_node],
                node.token
            )
        )

        self.visit(member_access_call_node)

    def visit_SplatArgument(self, node):
        # get variable
        value = self.visit(node.expr)

        if value is None:
            self.error(node, ErrorType.TypeError, 'cannot perform splat operation: value is null')
            return None

        if not isinstance(value, BasicValue):
            self.error(node, ErrorType.TypeError, 'cannot perform splat operation: value is not a BasicValue')
            return None

        extracted_value = value.extract_value()

        if not isinstance(extracted_value, list):
            self.error(node, ErrorType.TypeError, 'cannot perform splat operation: value must be an array')
            return None

        args = []

        # loop over each item in array and push to stack
        for item in extracted_value:
            args.append(BasicValue(item).extract_basicvalue())


        return args

    def visit_ArgumentList(self, node):
        # read arguments backwards as values are popped from stack
        for argument in reversed(node.arguments):
            # retrieve value
            value = self.stack.pop()
            # declare variable
            self.visit_Declare(argument)
            # set variable to passed in value
            if isinstance(value, AstNode):
                value = self.visit(value)

            if isinstance(argument, NodeSplatArgument):
                argument = NodeDeclare(None, argument.token, NodeNone(argument.token))
            self.current_scope.set_variable(argument.name.value, value)

    def visit_FunctionExpression(self, node):
        return node
    
    def visit_Macro(self, node):
        return self.visit(node.expr)

    def visit_Mixin(self, node):
        from parse.parser import Parser

        parser = Parser(node.tokens, self.source_location)
        
        ast = parser.parse()

        if len(parser.error_list.errors) > 0:
            self.error(node, ErrorType.MacroExpansionError, 'Macro expansion failed:\n{}'.format('\t'.join(map(lambda x: str(x), parser.error_list.errors))))
            return None

        last_value = None

        for node in ast:
            last_value = self.visit(node)

        return BasicValue(last_value).extract_basicvalue()

    def call_builtin_function(self, fun, this_object, arguments, node):
        basic_value_result = fun.call(BuiltinFunctionArguments(interpreter=self, this_object=this_object, arguments=arguments, node=node))

        if not isinstance(basic_value_result, BasicValue):
            self.error(node, ErrorType.TypeError, 'expected method {} to return an instance of BasicValue, got {}'.format(fun, basic_value_result))
            return None

        return basic_value_result

    def call_function_expression(self, node):
        # create our scope before block so argument variables are contained
        self.open_scope()
        function_scope = self.current_scope
        # visit our arguments
        self.visit(node.argument_list)
        # self.visit would normally be used here, but we need create_scope
        try:
            self.visit_Block(node.block, create_scope=False)
            # check if block contains a return statement
            last_child = None
            for child in node.block.children:
                last_child = child
                if isinstance(child, NodeFunctionReturn):
                    break

            # no return statement, push return code 0 to the stack
            if type(last_child) != NodeFunctionReturn:
                self.stack.push(BasicValue(0)) # should just be null or something
        except ReturnJump:
            # exit all enclosed scopes until the current scope
            # is equal to the same one we opened at the start of the function
            while self.current_scope != function_scope:
                self.close_scope()

        # done, close scope
        self.close_scope()

    def visit_ArrayExpression(self, node):
        if node.is_dictionary:
            members = {}

            for i in range(len(self.visit(node.members[0]).extract_value())):
                key = self.visit(self.visit(node.members[0]).extract_value()[i])
                value = self.visit(self.visit(node.members[1]).extract_value()[i])

                members[key] = value
        else:
            members = []

            for member_decl in node.members:
                value = self.visit(member_decl)

                members.append(value)

        return BasicValue(members)

    def visit_ObjectExpression(self, node):
        members = {}

        # open scope for members
        self.open_scope()

        for member_decl in node.members:
            value = self.visit(member_decl)

            members[member_decl.name.value] = value

        # close scope for members
        self.close_scope()

        return BasicObject(parent=None, members=members)

    def basic_value_to_object(self, node, target):
        # if not isinstance(target)
        target = BasicValue(target).extract_basicvalue()

        if not isinstance(target, BasicObject):
            target_type_object = target.lookup_type(self.global_scope).extract_basicvalue()

            if target_type_object is None:
                self.error(node, ErrorType.TypeError, 'invalid member access: target {} is not a BasicObject'.format(target))
                return None

            # for a string this would basically mean:
            # "hello ".append("world")
            # -> Str.new("hello ").append("world")
            target = builtin_object_new(BuiltinFunctionArguments(interpreter=self, this_object=target_type_object, arguments=[target], node=node))

        return target

    def walk_member_expression(self, node):
        target = self.visit(node.lhs)

        # if target is None:
        #     self.error(node, ErrorType.TypeError, 'invalid member access: {} has no member {}'.format(target, node.identifier))
        #     return None

        target = self.basic_value_to_object(node, target)

        member = target.lookup_member(node.identifier.value)

        if member is None:
            self.error(node, ErrorType.TypeError, '{} has no direct or inherited member `{}`'.format(obj_to_string(self, node, target), node.identifier.value))

        return (target, member)

    def visit_MemberExpression(self, node):
        return self.walk_member_expression(node)[1].value

    def visit_ArrayAccessExpression(self, node):
        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.lhs,
                LexerToken('__at__', TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [node.access_expr],
                node.token
            )
        )

        return self.visit(member_access_call_node)
        
    def visit_Empty(self, node):
        pass
    