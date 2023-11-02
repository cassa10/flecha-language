from enum import Enum


class Types(Enum):
    Char = "Char"
    Int = "Int"
    Struct = "Struct"
    Closure = "Closure"
    Void = "Void"


class Value:
    def __init__(self, _type):
        self.type = _type.value

    def is_closure(self):
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


class IntValue(LiteralValue):
    def __init__(self, value):
        super().__init__(Types.Int, value)


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
