import argparse
import os
import logger

from flecha.lexer import get_all_tokens, Lexer
from flecha.parser import Parser


def get_or_default(atr, default):
    atr_striped = atr.strip() if issubclass(type(atr), str) else atr
    if atr_striped in (None, ''):
        return default
    return atr


def get_main_args(arg_parser):
    # Inputs and outputs
    arg_parser.add_argument("-s", "--stringProgram", help="some valid string program")
    arg_parser.add_argument("-i", "--inputFile", help="path to input file with program")

    # TODO: generate output file
    #  argParser.add_argument("-o", "--outputFile", help="path to object output file")

    # Mode Tokenizer
    arg_parser.add_argument("-t", "--tokenize", action='store_true', help="Mode tokenize program input")

    # Debug
    arg_parser.add_argument("-d", "--debug", action='store_true',
                            help="Mode debug for watch program input and some debugging info")

    args = arg_parser.parse_args()

    if args.debug:
        print(f"Arguments: {args}")

    return (get_or_default(args.stringProgram, ''), args.tokenize, args.debug,
            get_or_default(args.inputFile, ''), get_or_default(args.stringProgram, ''))


def show_tokenize(_program_input, _show=False):
    if _show:
        print("[ Lexer Tokens ] => ")
        print(get_all_tokens(Lexer().build(), _program_input))
        print("\n")


def show_program_input(_program_input, _show=False):
    is_empty_program = _program_input == ""
    if _show or is_empty_program:
        logger.print("[ Program Input ] => ")
        logger.print(_program_input) if not is_empty_program else logger.warn('Empty program!!\n')
        logger.print("[ END Program Input]\n")


def read_input_file_or_default(filename: str, program_input_default: str) -> str:
    try:
        with open(os.path.join(os.getcwd(), filename), 'r') as fi:
            _program_input = fi.read()
            return _program_input if _program_input else program_input_default
    except Exception as e:
        logger.error(f"error when read file {filename} with exception {e}")
        logger.debug('using default program input')
        return program_input_default


if __name__ == "__main__":
    parser = Parser()
    parser.greet()

    # Get program arguments
    program_input, tokenize_mode, debug_mode, input_file, output_file = get_main_args(argparse.ArgumentParser())

    # Logger
    logger = logger.Logger(debug_mode)


    # override program_input with input_file if exists file
    program_input = read_input_file_or_default(input_file, program_input)

    # Optionals
    show_program_input(program_input, debug_mode)
    show_tokenize(program_input, tokenize_mode)

    # program = "def tres = \\\\1\t\n+2 \n --hola"
    # program = "def t1=a||b||c||d"
    program_ast = parser.parse(program_input)
    print("[ AST ] => ")
    print(f"{program_ast}")
