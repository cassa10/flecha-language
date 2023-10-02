from flecha.ast.ast_node import AstLeaf, AstLabel
from flecha.ast.expression import LambdaExpr


def create_expression(params, expression):
    if not params:
        return expression

    return LambdaExpr(params, create_expression(params[1::], expression))


def create_id(value):
    return AstLeaf(AstLabel.Id, value)
