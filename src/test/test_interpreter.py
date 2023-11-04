import pytest
from flecha.parser import Parser
from flecha.interpreter.package import Interpreter
from test.util_test import get_test_from_file
from io import StringIO
import sys

interpreter_tests_loc = "tests_interpreter*"
# Add test_name for create new tests of file (if file with desc index exist)
test_names = [
    'Print Char',
    'Print Number',
    'Print Number-From-Def',
    'Print from Let',
    'Print Hola Mundo',
    'Print numbers with lets',
    'Print secuence',
    'Print int lambda',
    'Print lambdas',
    'Print 42',
    'Test General functions',
    'Test Case',
    'Test Bools',
    'Test Prints',
    'Test Cases 2',
    'Map Structs',
    'Primitiva OR',
    'Primitiva AND',
    'Primitiva NOT',
    'Primitiva: EQ',
    'Primitiva: NE',
    'Primitiva: GE',
    'Primitiva: LE',
    'Primitiva: GT',
    'Primitiva: LT',
    'Primitiva: ADD',
    'Primitiva: SUB',
    'Primitiva: MUL',
    'Primitiva: DIV',
    'Primitiva: MOD',
    'Primitiva: UMINUS',
]


# use zfill for add 2 chars min padding of 0's at begin of number (eg: 0 -> 00, 1 -> 01, 12 -> 12)
@pytest.mark.parametrize('n, desc', [(f"{i+1}".zfill(2), e) for i, e in enumerate(test_names)])
def tests_parse_and_evaluate_from_files(n: str, desc: str):
    p = Parser()
    i = Interpreter()
    program_input, expected_out = __get_test_from_file_number(n)

    # Redirigir la salida
    original_stdout = sys.stdout
    sys.stdout = buffer = StringIO()

    program_ast = p.parse(program_input)
    i.eval(program_ast)

    # Restaurar la salida estándar original
    sys.stdout = original_stdout

    # Verificar la salida
    printed_content = buffer.getvalue()
    assert printed_content == expected_out



def test_parse_an_evaluate_only_with_n():
    """
    Only for debug an only test - for change file number change 'n' value
    :return:
    """
    n = 17
    p = Parser()
    i = Interpreter()
    program_input, expected_out = __get_test_from_file_number(n)

    # Redirigir la salida
    original_stdout = sys.stdout
    sys.stdout = buffer = StringIO()

    program_ast = p.parse(program_input)
    i.eval(program_ast)

    # Restaurar la salida estándar original
    sys.stdout = original_stdout

    # Verificar la salida
    printed_content = buffer.getvalue()
    assert printed_content == expected_out


def __get_test_from_file_number(number: str):
    return get_test_from_file(interpreter_tests_loc, number, file_extension='fl', json_format=False)
