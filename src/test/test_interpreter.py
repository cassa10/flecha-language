import pytest

from flecha.parser import Parser
from flecha.interpreter.package import Interpreter
from test.util_test import get_test_from_file

interpreter_tests_loc = "tests_interpreter*"

# Add test_name for create new tests of file (if file with desc index exist)
test_names = [
    'Print Char',
    'Print Number',
]


# use zfill for add 2 chars min padding of 0's at begin of number (eg: 0 -> 00, 1 -> 01, 12 -> 12)
@pytest.mark.parametrize('n, desc', [(f"{i+1}".zfill(2), e) for i, e in enumerate(test_names)])
def tests_parse_from_files(n: str, desc: str):
    p = Parser()
    i = Interpreter()
    program_input, expected_out = __get_test_from_file_number(n)
    program_ast = p.parse(program_input)
    assert i.eval(program_ast) == expected_out


def __get_test_from_file_number(number: str):
    return get_test_from_file(interpreter_tests_loc, number, file_extension='fl', json_format=False)
