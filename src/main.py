import argparse
import os

import logger
from config import Config
from flecha.interpreter.package import Interpreter
from flecha.lexer import get_all_tokens, Lexer
from flecha.parser import Parser
from repl import REPL


def read_input_file_or_default(filename: str, program_input_default: str) -> str:
    try:
        with open(os.path.join(os.getcwd(), filename), 'r') as fi:
            _program_input = fi.read()
            return _program_input if _program_input else program_input_default
    except Exception as e:
        logger.error(f"error when read file {filename} with exception {e}")
        logger.debug('using default program input')
        return program_input_default


def show_tokenize(_program_input, _show=False):
    if _show:
        logger.print("[ Lexer Tokens ] => \n")
        logger.print(get_all_tokens(Lexer().build(), _program_input))
        logger.print("\n[ END Lexer Tokens ]\n")


def show_program_input(_program_input, _show=False):
    is_empty_program = _program_input == ""
    if _show or is_empty_program:
        logger.print("[ Program Input ] => \n")
        logger.print(_program_input) if not is_empty_program else logger.warn('Empty program!!')
        logger.print("\n[ END Program Input]\n")


def show_parser_ast(_ast, _show=False):
    if _show:
        logger.print("[ AST Parsed ] => ")
        logger.print(f"{_ast}")
        logger.print("\n[ END AST Parsed ]\n")


if __name__ == "__main__":
    # Get config (or arguments)
    config = Config(argparse.ArgumentParser())

    if config.run_repl:
        REPL().run()
    else:
        # Logger
        logger = logger.Logger(config.debug_mode)

        # Init parser
        parser = Parser()
        parser.greet()

        # Override program_input with input_file if exists file
        program_input = read_input_file_or_default(config.program_from_file, config.program_from_str)

        # Optionals
        show_program_input(program_input, config.debug_mode)
        show_tokenize(program_input, config.tokenize_mode)

        program_ast = parser.parse(program_input)
        # TODO: when eval is done, then change "True" to "config.parser_mode "
        show_parser_ast(program_ast, config.parser_mode)

        interpreter = Interpreter()
        try:
            print(interpreter.eval(program_ast))
        except Exception as e:
            print(f'ERROR | {e}')

