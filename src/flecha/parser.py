from ply.yacc import yacc

from flecha.lexer import LexerFlecha


class Parser:

    def __init__(self):
        self.__lexer = LexerFlecha().build()
        self.__yacc = yacc

    def execute(self, program):
        self.__lexer.input(program)
        while True:
            token = self.__lexer.token()
            if not token:
                break
            print(token)

    def __str__(self):
        return 'Welcome to Flecha (=>) Language :D\n'
