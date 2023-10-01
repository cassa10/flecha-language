import glob
import json
import os

from flecha.ast.ast_node import jsonConfig


def get_input(filename):
    with open(os.path.join(os.getcwd(), filename), 'r') as fi:
        return fi.read()


def get_expected_out(filename):
    with open(os.path.join(os.getcwd(), filename[0:-5] + 'expected'), 'r') as fe:
        return json.dumps(json.loads(fe.read()), **jsonConfig)


def get_test_from_file(subfolder: str, number_of_test) -> (str, str):
    fullpath_file = glob.glob(os.getcwd() + f'/**/{subfolder}/test{number_of_test}.input', recursive=True)[0]
    return get_input(fullpath_file), get_expected_out(fullpath_file)
