import os

from typing import Callable
import logger
from flecha.interpreter.package import Interpreter
from flecha.lexer import get_all_tokens, Lexer
from flecha.parser import Parser


class Execution:

    def __init__(self, config):
        self.config = config
        self.logger = logger.Logger(config.debug_mode)
        self.parser = Parser()
        self.intpr = Interpreter()

        self.is_show_program_input = config.debug_mode
        self.is_show_tokenize = config.tokenize_mode
        self.is_parser_mode = config.parser_mode

    def execute(self):
        self.parser.greet()

        # Override program_input with input_file if exists file
        program_input = self.read_input_file_or_default(
            self.config.program_from_file,
            self.config.program_from_str
        )

        # Optionals
        self.show_program_input(program_input)
        self.show_tokenize(program_input)
        program_ast = self.parser.parse(program_input)

        # TODO: Only Parser mode?? or only show??
        self.show_parser_ast(program_ast)

        # TODO: Handle output param at file

        try:
            print(self.intpr.eval(program_ast))
        except Exception as e:
            print(f'ERROR | {e}')

    def read_input_file_or_default(self, _filename: str, program_input_default: str) -> str:
        filename = _filename.lstrip()
        if filename == '':
            return program_input_default
        try:
            with open(os.path.join(os.getcwd(), filename), 'r') as fi:
                _program_input = fi.read()
                return _program_input if _program_input else program_input_default
        except Exception as e:
            self.logger.error(f"error when read file {filename} with exception {e}")
            self.logger.debug('using default program input')
            return program_input_default


    def show_tokenize(self, _program_input):
        label = 'Lexer Tokens'
        self.__logger_wrapper(
            self.is_show_tokenize, label, label,
            lambda: self.logger.print(get_all_tokens(Lexer().build(), _program_input))
        )

    def show_program_input(self, _program_input):
        is_empty_program = _program_input == ""
        label = 'Program Input'
        self.__logger_wrapper(
            self.is_show_program_input or is_empty_program, label, label,
            lambda: self.logger.print(_program_input) if not is_empty_program else self.logger.warn('Empty program!!')
        )

    def show_parser_ast(self, ast):
        label = 'AST Parsed'
        self.__logger_wrapper(
            self.is_parser_mode, label, label,
            lambda: self.logger.print(f"{ast}")
        )

    # show
    def __logger_wrapper(self, show: bool, header_str: str, footer_str: str, fn: Callable[[], None]):
        if show:
            self.logger.print(f"{{ {header_str} }} => \n")
            fn()
            self.logger.print(f"\n{{ END {footer_str} }}\n")
