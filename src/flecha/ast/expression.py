from flecha.ast.ast_node import AstNode, AstLabel, AstLeaf

atomic_expr = {
    "LOWERID": lambda v: VarExpr(v),
    "UPPERID": lambda v: ExprConstructor(v),
    "NUMBER": lambda v: NumberExpr(v),
    "CHAR": lambda v: CharExpr(v),
    "STRING": lambda v: StringExpr(v),
}


class Expression(AstNode):
    def __init__(self, label: AstLabel, expr):
        super().__init__(label, expr)

    def _out(self):
        return [self.label, self.children]


class LambdaExpr(Expression):
    def __init__(self, params, expr):
        super().__init__(AstLabel.ExprLambda, expr)
        self.params = params


class NumberExpr(Expression):
    def __init__(self, value):
        super().__init__(AstLabel.ExprNumber, value)


class VarExpr(Expression):
    def __init__(self, value):
        super().__init__(AstLabel.ExprVar, create_id(value))


class ExprConstructor(Expression):
    def __init__(self, value):
        super().__init__(AstLabel.ExprConstructor, create_id(value))


class CharExpr(Expression):
    def __init__(self, value):
        pass


class StringExpr(Expression):
    def __init__(self, value):
        pass


# Builders

def create_expression(params, expression):
    if not params:
        return expression

    return LambdaExpr(params, create_expression(params[1::], expression))


def create_id(value):
    return AstLeaf(AstLabel.Id, value)


def create_atomic(_type, value):
    return atomic_expr[_type](value)
