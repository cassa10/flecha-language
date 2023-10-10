from ply.yacc import yacc

from flecha.ast.expression import *
from flecha.ast.program import Program, Def
from flecha.lexer import Lexer


class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD')
    )

    def __init__(self):
        self.__lexer = Lexer().build()
        self.__yacc = yacc(module=self)

    def p_program_empty(self, p):
        """program :"""
        p[0] = Program()

    def p_program(self, p):
        """program : program definition"""
        program = p[1]
        p[0] = program.append(p[2])

    def p_def(self, p):
        """definition : DEF LOWERID parameters DEFEQ expression"""
        p[0] = Def(p[2], build_expression(p[3], p[5]))

    def p_parameters_empty(self, p):
        """parameters :"""
        p[0] = []

    def p_parameters(self, p):
        """parameters :  parameters LOWERID"""
        p[0] = p[1] + [p[2]]

    # TODO: Cambiar applyExpr (Se lo pone para incrementar de a poco las producciones)
    def p_expression(self, p):
        """expression : applyExpr"""
        p[0] = p[1]

    def p_applyExpression_base(self, p):
        """applyExpr : atomicExpr"""
        p[0] = p[1]

    def p_applyExpression(self, p):
        """applyExpr : applyExpr atomicExpr"""
        p[0] = ApplyExpr(p[1], p[2])

    def p_atomicExpr(self, p):
        """atomicExpr : LOWERID
                        | UPPERID
                        | NUMBER
                        | CHAR
                        | STRING"""
        p[0] = build_atomic(p.slice[1].type, p[1])

    def p_atomicExpr_paren(self, p):
        """atomicExpr : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_error(self, p):
        print(f'Syntax error: {p.value!r} | At line: {p.lineno}')

    def parse(self, input):
        output = self.__yacc.parse(input, lexer=self.__lexer)
        return output

    def __str__(self):
        return 'Welcome to Flecha (=>) Language :D\n'
