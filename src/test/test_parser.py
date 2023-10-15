import pytest

from flecha.parser import Parser
from test.util_test import get_test_from_file

parser_tests_loc = "tests_parser*"

# Add test_name for create new tests of file (if file with desc index exist)
test_names = [
    'Empty Program',
    'Numbers',
    'Variables',
    'Constructors',
    'Characters',
    'Structures',
    'Strings',
    'If',
    'Case',
    'Apply',
    'Local Declarations',
    'Anonymous functions',
    'Sequencing',
    'Control Structure Nesting',
    'Operators',
    'Associativity',
    'Operators/Apply Nesting',
    'Precedence',
    'Some program',
]


# use zfill for add 2 chars min padding of 0's at begin of number (eg: 0 -> 00, 1 -> 01, 12 -> 12)
@pytest.mark.parametrize('n, desc', [(f"{i}".zfill(2), e) for i, e in enumerate(test_names)])
def tests_parse_from_files(n: str, desc: str):
    p = Parser()
    program_input, expected_out = __get_test_from_file_number(n)
    assert f'{p.parse(program_input)}' == expected_out


def __get_test_from_file_number(number: str):
    return get_test_from_file(parser_tests_loc, number)
