from flecha.ast_impl.ast_node import AstNode, AstLabel, AstLeaf

# used for create strings with list structures of chars
LIST_APPENDER = 'Cons'
LIST_EMPTY = 'Nil'
BLANK_VAR = '_'

atomic_expr = {
    "LOWERID": lambda v: VarExpr(v),
    "UPPERID": lambda v: ConstructorExpr(v),
    "NUMBER": lambda v: NumberExpr(v),
    "CHAR": lambda v: CharExpr(v),
    "STRING": lambda v: build_string(v),
}

OP_UNARY = 'unary'
OP_BINARY = 'binary'

MAPPED_UNARY_NOT = '!'
MAPPED_UNARY_MINUS = '-'

UNARY_NOT = 'NOT'
UNARY_MINUS = 'UMINUS'

MAPPED_BINARY_OR = '||'
MAPPED_BINARY_AND = '&&'
MAPPED_BINARY_EQ = '=='
MAPPED_BINARY_NE = '!='
MAPPED_BINARY_GE = '>='
MAPPED_BINARY_LE = '<='
MAPPED_BINARY_GT = '>'
MAPPED_BINARY_LT = '<'
MAPPED_BINARY_ADD = '+'
MAPPED_BINARY_SUB = '-'
MAPPED_BINARY_MUL = '*'
MAPPED_BINARY_DIV = '/'
MAPPED_BINARY_MOD = '%'

BINARY_OR = 'OR'
BINARY_AND = 'AND'
BINARY_EQ = 'EQ'
BINARY_NE = 'NE'
BINARY_GE = 'GE'
BINARY_LE = 'LE'
BINARY_GT = 'GT'
BINARY_LT = 'LT'
BINARY_ADD = 'ADD'
BINARY_SUB = 'SUB'
BINARY_MUL = 'MUL'
BINARY_DIV = 'DIV'
BINARY_MOD = 'MOD'


operators = {
    OP_BINARY: {
        MAPPED_BINARY_OR: BINARY_OR,
        MAPPED_BINARY_AND: BINARY_AND,
        MAPPED_BINARY_EQ: BINARY_EQ,
        MAPPED_BINARY_NE: BINARY_NE,
        MAPPED_BINARY_GE: BINARY_GE,
        MAPPED_BINARY_LE: BINARY_LE,
        MAPPED_BINARY_GT: BINARY_GT,
        MAPPED_BINARY_LT: BINARY_LT,
        MAPPED_BINARY_ADD: BINARY_ADD,
        MAPPED_BINARY_SUB: BINARY_SUB,
        MAPPED_BINARY_MUL: BINARY_MUL,
        MAPPED_BINARY_DIV: BINARY_DIV,
        MAPPED_BINARY_MOD: BINARY_MOD
    },
    OP_UNARY: {
        MAPPED_UNARY_MINUS: UNARY_MINUS,
        MAPPED_UNARY_NOT: UNARY_NOT
    }
}


class LetExpr(AstNode):
    def __init__(self, _id: str, expr1, expr2):
        super().__init__(AstLabel.ExprLet, [build_id(_id), expr1, expr2])

    def param(self):
        return self.children[0].value

    def arg(self):
        return self.children[1]

    def expr_in(self):
        return self.children[2]


class ApplyExpr(AstNode):
    def __init__(self, func, arg):
        super().__init__(AstLabel.ExprApply, [func, arg])

    def func(self):
        return self.children[0]

    def arg(self):
        return self.children[1]


class LambdaExpr(AstNode):
    def __init__(self, param, expr):
        super().__init__(AstLabel.ExprLambda, [build_id(param), expr])

    def param(self):
        return self.children[0].value

    def expr(self):
        return self.children[1]


class LiteralExpr(AstLeaf):
    def __init__(self, label: AstLabel, value):
        super().__init__(label, value)

    def _out(self):
        return [self.label, self.value]


class NumberExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprNumber, value)


class VarExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprVar, build_id(value))

    def id(self):
        return self.value.value


class ConstructorExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprConstructor, build_id(value))

    def id(self):
        return self.value.value


class CharExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprChar, ord(value))


# Builders
def build_seq_let(expr1, expr2):
    return LetExpr(BLANK_VAR, expr1, expr2)


def build_expression(params, expression):
    if not params:
        return expression
    return LambdaExpr(params[0], build_expression(params[1::], expression))


def build_id(value: str):
    return AstLeaf(AstLabel.Id, value)


def build_atomic(_type, value):
    return atomic_expr[_type](value)


def build_binary_expression(left, operator, right):
    op = operators[OP_BINARY].get(operator)
    left_apply = ApplyExpr(VarExpr(op), left)
    return ApplyExpr(left_apply, right)


def build_unary_expression(operator, right):
    op = operators[OP_UNARY].get(operator)
    return ApplyExpr(VarExpr(op), right)


def build_string(string_param: str):
    if not string_param:
        return ConstructorExpr(LIST_EMPTY)
    return (
        ApplyExpr(
            ApplyExpr(
                ConstructorExpr(LIST_APPENDER),
                CharExpr(string_param[0])
            ),
            build_string(string_param[1:])
        )
    )
