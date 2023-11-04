import json
import uuid
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
    Null = "Null"


class Value:
    def __init__(self, _type=Types.Null):
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

    def __repr__(self):
        return f"{self.type}"


class VoidValue(Value):
    def __init__(self):
        super().__init__(Types.Void)

    def __repr__(self):
        return self.type


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

    def __neg__(self):
        return IntValue(self.value) * IntValue(-1)

    def __eq__(self, other):
        return BoolValue(self.value == other.value)

    def __ne__(self, other):
        return BoolValue(self.value != other.value)

    def __lt__(self, other):
        return BoolValue(self.value < other.value)

    def __le__(self, other):
        return BoolValue(self.value <= other.value)

    def __gt__(self, other):
        return BoolValue(self.value > other.value)

    def __ge__(self, other):
        return BoolValue(self.value >= other.value)

    def __add__(self, other):
        return IntValue(self.value + other.value)

    def __sub__(self, other):
        return IntValue(self.value - other.value)

    def __mul__(self, other):
        return IntValue(self.value * other.value)

    def __mod__(self, other):
        return IntValue(self.value % other.value)

    def __truediv__(self, other):
        return IntValue(int(self.value / other.value))


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

    def __repr__(self):
        return f"{self.type}#{id(self)}"


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

    def __repr__(self):
        if self.constructor in BOOL_VALUES:
            return self.constructor
        return json.dumps([self.constructor] + self.args, default=str)


class BoolValue(StructValue):
    def __init__(self, _bool):
        super().__init__(BOOL_TRUE if _bool else BOOL_FALSE, [])
