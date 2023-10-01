import json
from typing import Sequence
from enum import Enum

# TODO: Move all Json to another class or file??
jsonConfig = dict(separators=(',', ':'), default=lambda obj: obj.value)
def flecha_json_decode(out):
    return json.dumps(out, **jsonConfig)


AstNodeOutput = int | str | Sequence['AstNodeOutput']


class AstLabel(Enum):
    Program = ""
    ExprNumber = "ExprNumber"


class AstNode:

    def __init__(self, label: AstLabel, children):
        self.label = label
        self.children: list['AstNode'] = children

    def append(self, child: 'AstNode') -> 'AstNode':
        self.children.append(child)
        return self

    def _out(self) -> AstNodeOutput:
        return [self.label] + self._children_out()

    def _children_out(self):
        return [c._out() for c in self.children]

    def __repr__(self) -> str:
        return flecha_json_decode(self._out())

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()


class AstLeaf(AstNode):
    def __init__(self, label: AstLabel, value):
        super().__init__(label, None)
        self.value = value

    def _out(self) -> AstNodeOutput:
        return self.value


class AstNodeList(AstNode):
    def __init__(self, label: AstLabel, nodes: Sequence[AstNode]):
        super().__init__(label, nodes)

    def _out(self) -> AstNodeOutput:
        if self.children:
            return self.children
        else:
            return []


class Program(AstNodeList):

    def __init__(self):
        super().__init__(AstLabel.Program, [])
