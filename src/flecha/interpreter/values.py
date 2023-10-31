from enum import Enum


class Types(Enum):
    Char = "Char"
    Int = "Int"
    Struct = "Struct"
    Closure = "Closure"



class Value:
    pass


class VoidValue(Value):
    # eg: unsafePrintInt('2')
    pass


class LiteralValue(Value):
    def __init__(self, _type: Types, v):
        self.type = _type.value
        self.value = v

    def __repr__(self):
        return f"{self.value}"


class CharValue(LiteralValue):
    def __init__(self, value):
        super().__init__(Types.Char, chr(value))


class IntValue(LiteralValue):
    def __init__(self, value):
        super().__init__(Types.Int, value)

