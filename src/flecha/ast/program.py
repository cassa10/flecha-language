from flecha.ast.ast_node import AstNodeList, AstLabel


class Program(AstNodeList):

    def __init__(self):
        super().__init__(AstLabel.Program, [])