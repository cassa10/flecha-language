from ply.yacc import yacc

from flecha.ast.expression import create_expression, create_atomic
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
        """definition : DEF LOWERID parameters DEFEQ atomicExpr"""
        p[0] = Def(p[2], create_expression(p[3], p[5]))

    def p_parameters_empty(self, p):
        """parameters :"""
        p[0] = []

    def p_parameters(self, p):
        """parameters :  parameters LOWERID"""
        p[0] = p[1] + [p[2]]

    def p_binaryExpr(self, p):
        """ binaryExpr : atomicExpr AND atomicExpr
                             | atomicExpr OR atomicExpr
                             | atomicExpr EQ atomicExpr
                             | atomicExpr NE atomicExpr
                             | atomicExpr GE atomicExpr
                             | atomicExpr LE atomicExpr
                             | atomicExpr GT atomicExpr
                             | atomicExpr LT atomicExpr
                             | atomicExpr PLUS atomicExpr
                             | atomicExpr MINUS atomicExpr
                             | atomicExpr TIMES atomicExpr
                             | atomicExpr DIV atomicExpr
                             | atomicExpr MOD atomicExpr"""
        p[0] = f"[{p[1]} {p[2]} {p[3]}]"

    def p_atomicExpr(self, p):
        """atomicExpr : LOWERID
                        | UPPERID
                        | NUMBER
                        | CHAR
                        | STRING"""
        p[0] = create_atomic(p.slice[1].type, p[1])

    # def p_atomicExpr_paren(self, p):
    #     """atomicExpr : LPAREN expression RPAREN"""
    #     pass

    def p_error(self, p):
        print(f'Syntax error: {p.value!r} | At line: {p.lineno}')

    def parse(self, input):
        output = self.__yacc.parse(input, lexer=self.__lexer)
        return output

    def __str__(self):
        return 'Welcome to Flecha (=>) Language :D\n'
