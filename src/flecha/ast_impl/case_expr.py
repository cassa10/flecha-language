from typing import Sequence

from flecha.ast_impl.ast_node import AstNodeList, AstNode
from flecha.ast_impl.expression import build_id
from flecha.ast_impl.label import AstLabel

TRUE_ID = 'True'
FALSE_ID = 'False'


class CaseBranch(AstNode):
    def __init__(self, _id: str, _params: Sequence[str], expr):
        super().__init__(AstLabel.CaseBranch, [build_id(_id), Params([build_id(param) for param in _params]), expr])

    def id(self):
        return self.children[0].value

    def params(self):
        return [param.value for param in self.children[1].children]

    def expr(self):
        return self.children[2]

class Params(AstNodeList):
    def __init__(self, params):
        super().__init__(AstLabel.Params, params)


class CaseBranches(AstNodeList):
    def __init__(self, branches: Sequence[CaseBranch]):
        super().__init__(AstLabel.CaseBranches, branches)

    def append_case(self, branch):
        return self.append(branch)


class CaseExpr(AstNode):
    def __init__(self, expr: AstNode, branches: CaseBranches):
        super().__init__(AstLabel.ExprCase, [expr] + branches.children)

    def expr(self):
        return self.children[0]

    def branches(self):
        return self.children[1:]

    def _out_branches(self):
        return [b._out() for b in self.branches()]

    def _out(self):
        return [self.label, self.expr()._out(), self._out_branches()]

# Builders

def build_if(expr, then_expr, else_expr):
    return CaseExpr(expr, CaseBranches([CaseBranch(TRUE_ID, [], then_expr), else_expr]))


def build_else(else_expr):
    return CaseBranch(FALSE_ID, [], else_expr)
