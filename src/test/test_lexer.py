import pytest

from flecha.lexer import Lexer as FlechaLexer, get_all_tokens

# Data is {<test-name>: (program, expected_tokens), ...}
lexer_tests = {
    "Comment": ("--Hola def uno = 1 + 3 \\ \t asd\n", []),
    "Char": ("\'a\'", [('CHAR', 'a')]),
    "Char newline": ("\'\\n\'", [('CHAR', '\n')]),
    "String": ("\"asD123\r\t\n\"", [('STRING', 'asD123\r\t\n')]),
    "Lower Id": ("x1 == x2", [('LOWERID', 'x1'), ('EQ', '=='), ('LOWERID', 'x2')]),
    "Upper Id": ("Y1 == Y2", [('UPPERID', 'Y1'), ('EQ', '=='), ('UPPERID', 'Y2')]),
    "Semicolon": (";", [('SEMICOLON', ';')]),
    "Left Paren": ("(", [('LPAREN', '(')]),
    "Right Paren": (")", [('RPAREN', ')')]),
    "Lambda": ("\\", [('LAMBDA', '\\')]),
    "Arrow": ("->", [('ARROW', '->')]),
    "And Operator": ("&&", [('AND', '&&')]),
    "Or Operator": ("||", [('OR', '||')]),
    "Not Operator": ("!", [('NOT', '!')]),
    "Equals": ("==", [('EQ', '==')]),
    "Not Equals": ("!=", [('NE', '!=')]),
    "Great Than or Equal": (">=", [('GE', '>=')]),
    "Less Than or Equal": ("<=", [('LE', '<=')]),
    "Strict Greater Than": (">", [('GT', '>')]),
    "Strict Less Than": ("<", [('LT', '<')]),
    "Plus Op": ("+", [('PLUS', "+")]),
    "Minus Op": ("-", [('MINUS', "-")]),
    "Times": ("*", [('TIMES', "*")]),
    "Division": ("/", [('DIV', "/")]),
    "Modulo": ("%", [('MOD', "%")]),
    "Pipe": ("|", [('PIPE', '|')]),
    "Definition Equal": ("=", [('DEFEQ', "=")]),
    "Def": ("def", [('DEF', 'def')]),
    "If": ("if", [('IF', 'if')]),
    "Then": ("then", [('THEN', 'then')]),
    "Elif": ("elif", [('ELIF', 'elif')]),
    "Else": ("else", [('ELSE', 'else')]),
    "Case": ("case", [('CASE', 'case')]),
    "Let": ("let", [('LET', 'let')]),
    "In": ("in", [('IN', 'in')]),
    "Expr Plus": ("3 + 1",
        [('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 1)]
    ),
    "Expr Minus": ("10 - 255",
       [('NUMBER', 10), ('MINUS', '-'), ('NUMBER', 255)]
    ),
    "Expr Def": ("def uno\t =\n 1 \n\t + \t\n 3\n",
        [('DEF', 'def'), ('LOWERID', 'uno'), ('DEFEQ', '='), ('NUMBER', 1), ('PLUS', '+'), ('NUMBER', 3)]
     ),
    "Comment between lines": (
        "2 + 3 --Asd def 123+= 2 || \n --Hola \\ \t asd\n 0 + 1",
        [('NUMBER', 2), ('PLUS', '+'), ('NUMBER', 3), ('NUMBER', 0), ('PLUS', '+'), ('NUMBER', 1)]
    ),
}


@pytest.mark.parametrize(
    'program, expected',
    [(program, expected) for _, (program, expected) in enumerate(lexer_tests.values())],
    ids=[f"Test {i + 1} | {test_name}" for i, test_name in enumerate(lexer_tests.keys())]
)
def tests_lexer(program, expected):
    tokens = __init_lexer_and_get_tokens(program)
    assert tokens == expected


def __init_lexer_and_get_tokens(program):
    return get_all_tokens(FlechaLexer().build(), program)
