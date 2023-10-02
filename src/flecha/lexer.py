import ply.lex as ply_lex
from ply.lex import Lexer as PlyLexer
import re


def get_all_tokens(lexer: PlyLexer, program):
    res = []
    lexer.input(program)
    while True:
        token = lexer.token()
        if not token:
            break
        res.append((token.type, token.value))
    return res


class Lexer:
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

    tokens = tokens + list(keywords.values())

    t_ignore = ' \t'

    t_SEMICOLON = r';'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

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

    t_PIPE = r'\|'

    # Must be in the end for no conflicts
    t_DEFEQ = r'='

    # escaped chars \n, \t, \r, \, ', "
    esc_regex = re.compile(r"(?P<esc>\\[ntr\\\'\"])")

    esc_chars = {
        "\\n": '\n',
        "\\r": '\r',
        "\\t": '\t',
        "\\\\": '\\',
        '\\"': '"',
        "\\'": "'"
    }

    def t_CHAR(self, t):
        r"""\'(?P<value>(\\[ntr\\\'\"])|[^\\\'])\'"""
        val = t.lexer.lexmatch.group('value')
        if val in Lexer.esc_chars:
            t.value = Lexer.esc_chars[val]
        else:
            t.value = val
        return t

    def t_STRING(self, t):
        r"""\"(?P<value>((\\[ntr\\\'\"])|[^\\\"])*)\""""
        string_value = re.sub(
            Lexer.esc_regex,
            lambda x: Lexer.esc_chars[x.group('esc')], t.lexer.lexmatch.group('value')
        )
        t.value = string_value
        return t

    def t_LOWERID(self, t):
        r"""[a-z][_a-zA-Z0-9]*"""
        t.type = Lexer.keywords.get(t.value, 'LOWERID')
        return t

    def t_UPPERID(self, t):
        r"""[A-Z][_a-zA-Z0-9]*"""
        t.type = Lexer.keywords.get(t.value, 'UPPERID')
        return t

    def t_NUMBER(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_comment(self, t):
        r"""\--.*\n?"""
        t.lexer.lineno += 1

    def t_ignore_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

    def build(self) -> PlyLexer:
        return ply_lex.lex(module=self)
