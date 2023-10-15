from flecha.ast.ast_node import AstNode, AstLabel, AstLeaf, AstNodeList

# used for create strings with list structures of chars
LIST_APPENDER = 'Cons'
LIST_EMPTY = 'Nil'

atomic_expr = {
    "LOWERID": lambda v: VarExpr(v),
    "UPPERID": lambda v: ConstructorExpr(v),
    "NUMBER": lambda v: NumberExpr(v),
    "CHAR": lambda v: CharExpr(v),
    "STRING": lambda v: build_string(v),
}


class ApplyExpr(AstNode):

    def __init__(self, func, arg):
        super().__init__(AstLabel.ExprApply, [func, arg])


class LambdaExpr(AstNode):
    def __init__(self, params, expr):
        super().__init__(AstLabel.ExprLambda, expr)
        self.params = params


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


class ConstructorExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprConstructor, build_id(value))


class CharExpr(LiteralExpr):
    def __init__(self, value):
        super().__init__(AstLabel.ExprChar, ord(value))


# Builders

def build_expression(params, expression):
    if not params:
        return expression
    return LambdaExpr(params, build_expression(params[1::], expression))


def build_id(value: str):
    return AstLeaf(AstLabel.Id, value)


def build_atomic(_type, value):
    return atomic_expr[_type](value)


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
