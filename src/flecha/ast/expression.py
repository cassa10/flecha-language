from flecha.ast.ast_node import AstNode, AstLabel, AstLeaf


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





