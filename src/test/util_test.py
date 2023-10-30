import glob
import json
import os

from flecha.ast_impl.ast_node import jsonConfig


def get_input(filename):
    with open(os.path.join(os.getcwd(), filename), 'r') as fi:
        return fi.read()


def get_expected_out(filename, extension_len):
    with open(os.path.join(os.getcwd(), filename[0:(-1*extension_len)] + 'expected'), 'r') as fe:
        return fe.read()


def get_test_from_file(subfolder: str, number_of_test, file_extension='input', json_format=False) -> (str, str):
    fullpath_file = glob.glob(os.getcwd() + f'/**/{subfolder}/test{number_of_test}.{file_extension}', recursive=True)[0]
    expected_out = get_expected_out(fullpath_file, len(file_extension))
    expected_out = json.dumps(json.loads(expected_out), **jsonConfig) if json_format else expected_out
    return get_input(fullpath_file), expected_out
