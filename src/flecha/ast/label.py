from enum import Enum


class AstLabel(Enum):
    Program = ""
    Id = "Id"
    ExprNumber = "ExprNumber"
    ExprLambda = "ExprLambda"
    Def = "Def"