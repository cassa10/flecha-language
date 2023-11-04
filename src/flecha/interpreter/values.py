from enum import Enum

MAIN_DEF = 'main'

UNSAFE_PRINT_INT = 'unsafePrintInt'
UNSAFE_PRINT_CHAR = 'unsafePrintChar'

BOOL_FALSE = 'False'
BOOL_TRUE = 'True'
BOOL_VALUES = [BOOL_FALSE, BOOL_TRUE]

class Types(Enum):
    Char = "Char"
    Int = "Int"
    Struct = "Struct"
    Closure = "Closure"
    Void = "Void"
    Bool = "Boolean"


class Value:
    def __init__(self, _type):
        self.type = _type.value

    def is_closure(self):
        return False

    def is_char(self):
        return False

    def is_int(self):
        return False

    def is_struct_type(self):
        return False

    def is_bool(self):
        return False


class VoidValue(Value):
    def __init__(self):
        super().__init__(Types.Void)


class LiteralValue(Value):
    def __init__(self, _type: Types, v):
        super().__init__(_type)
        self.value = v

    def __repr__(self):
        return f"{self.value}"


class CharValue(LiteralValue):
    def __init__(self, value):
        super().__init__(Types.Char, chr(value))

    def is_char(self):
        return True


class IntValue(LiteralValue):
    def __init__(self, value):
        super().__init__(Types.Int, value)

    def is_int(self):
        return True


class ClosureValue(Value):
    def __init__(self, param, body, env):
        super().__init__(Types.Closure)
        self.param = param
        self.body = body
        self.env = env

    def extend_env(self, param, arg):
        return self.env.extend(param, arg)

    def is_closure(self):
        return True


class StructValue(Value):
    def __init__(self, constructor, args):
        super().__init__(Types.Struct)
        self.constructor = constructor
        self.args = args

    def get_arg(self, i):
        return self.args[i]

    def args_len(self):
        return len(self.args)

    def is_struct_type(self):
        return True


class BoolValue(StructValue):
    def __init__(self, _bool):
        super().__init__(BOOL_TRUE if _bool else BOOL_FALSE, [])