from ply.yacc import yacc

from flecha.lexer import LexerFlecha

class Parser:
    tokens = LexerFlecha.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD')
    )

    def __init__(self):
        self.__lexer = LexerFlecha().build()
        self.__yacc = yacc(module=self)

    def execute(self, program):
        self.__lexer.input(program)
        while True:
            token = self.__lexer.token()
            if not token:
                break
            print(token)

    def p_program_empty(self, p):
        """program :"""
        p[0] = "[]"

    def p_program(self, p):
        """program : binaryExpr"""
        p[0] = f"[{p[1]}]"

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

    def p_atomicExpr_number(self, p):
        """atomicExpr : NUMBER"""
        p[0] = p[1]

    def p_error(self, p):
        print(f'Syntax error: {p.value!r} | At line: {p.lineno}')

    def parse(self, input):
        output = self.__yacc.parse(input, lexer=self.__lexer)
        return output

    def __str__(self):
        return 'Welcome to Flecha (=>) Language :D\n'
