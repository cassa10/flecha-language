import json
from typing import Sequence

# TODO: Move all Json to another class or file??
from flecha.ast_impl.label import AstLabel

jsonConfig = dict(separators=(',', ':'), default=lambda obj: obj.value)


def flecha_json_encode(out):
    return json.dumps(out, **jsonConfig)


AstNodeOutput = int | str | Sequence['AstNodeOutput']


class AstNode:

    def __init__(self, label: AstLabel, children):
        self.value = None
        self.label = label
        self.children: list['AstNode'] = children

    def append(self, child: 'AstNode') -> 'AstNode':
        self.children.append(child)
        return self

    def _out(self):
        return [self.label] + self._children_out()

    def _children_out(self):
        return [c._out() for c in self.children]

    def __repr__(self) -> str:
        return flecha_json_encode(self._out())

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()


class AstLeaf(AstNode):
    def __init__(self, label: AstLabel, value):
        super().__init__(label, None)
        self.value = "OR" if value == '||' else value

    def _out(self) -> AstNodeOutput:
        return self.value


class AstNodeList(AstNode):
    def __init__(self, label: AstLabel, nodes: Sequence[AstNode]):
        super().__init__(label, nodes)

    def _out(self) -> AstNodeOutput:
        return self._children_out() if self.children else []
