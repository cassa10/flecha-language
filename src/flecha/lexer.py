import ply.lex as ply_lex
from ply.lex import Lexer as PlyLexer


class LexerFlecha:
    tokens = [
        # Identifiers
        'LOWERID', 'UPPERID',

        # Constants
        'NUMBER', 'CHAR', 'STRING',

        # RESERVED SYMBOLS

        # Delimiters
        'DEFEQ', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LAMBDA', 'PIPE', 'ARROW',

        # Boolean Operators
        'AND', 'OR', 'NOT',

        # Relational Operators
        'EQ', 'NE', 'GE', 'LE', 'GT', 'LT',

        # Arithmetic Operators
        'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
    ]

    keywords = {
        'def': 'DEF',
        'if': 'IF',
        'then': 'THEN',
        'elif': 'ELIF',
        'else': 'ELSE',
        'case': 'CASE',
        'let': 'LET',
        'in': 'IN',
    }

    t_ignore = ' \t'

    t_SEMICOLON = r';'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_PIPE = r'\|'
    t_ARROW = r'->'
    t_LAMBDA = r'(\\)'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'

    t_EQ = r'=='
    t_NE = r'!='
    t_GE = r'>='
    t_LE = r'<='
    t_GT = r'>'
    t_LT = r'<'

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'

    # Must be in the end for no conflicts
    t_DEFEQ = r'='

    def t_NUMBER(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

    def build(self) -> PlyLexer:
        return ply_lex.lex(module=self)
