from flecha.ast_impl.ast_node import AstNodeList, AstLabel, AstNode
from flecha.ast_impl.expression import build_id


class Program(AstNodeList):
    def __init__(self):
        super().__init__(AstLabel.Program, [])


class Def(AstNode):
    def __init__(self, id_value, expr):
        super().__init__(AstLabel.Def, [build_id(id_value), expr])
