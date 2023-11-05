import os
import sys

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

        self.program_from_str = self.config.program_from_str
        self.program_from_file = self.config.program_from_file.lstrip()
        self.program_output_filename = self.config.output_file.strip()

        self.is_show_program_input = config.debug_mode
        self.is_show_tokenize = config.show_tokens
        self.is_show_parser_ast = config.show_parser_ast

        # Execute Priority
        self.tokenizer_mode = self.config.run_tokenize_mode
        self.parser_mode = self.config.run_parse_mode

    def execute(self):
        self.parser.greet()

        # Get program from input_file if exists file
        #   Otherwise get program from -s flag
        program_input = self.get_program_input()

        self.show_program_input(program_input)
        tokens = self.tokenize(program_input)
        program_ast = self.parser.parse(program_input)
        self.show_parser_ast(program_ast)

        # Priority: Tokens -> Parsed AST -> Evaluation (depend on active flag commands)
        func = (lambda: self.logger.print(program_ast)) if self.parser_mode else \
            (lambda: self.eval_program(program_ast))
        func = (lambda: self.logger.print(tokens)) if self.tokenizer_mode else func

        # Eval and handle output
        self.handle_output(program_ast, func)

    def handle_output(self, program_ast, func: Callable[[], None]):
        if self.program_output_filename == '':
            try:
                self.logger.debug(
                    f"No write or generate output file because empty or invalid filename '{self.program_output_filename}'")
                self.logger.print(func())
            except Exception as e:
                self.logger.print(f'EVAL ERROR | {e}')
        else:
            self.write_output_file(func)

    def eval_program(self, program_ast):
        self.intpr.eval(program_ast)

    def get_program_input(self) -> str:
        filename = self.program_from_file
        program_input_default = self.program_from_str
        if filename == '':
            self.logger.debug('using default program input (-s | --stringProgram)')
            return program_input_default
        try:
            with open(os.path.join(os.getcwd(), filename), 'r') as fi:
                _program_input = fi.read()
                return _program_input if _program_input else program_input_default
        except Exception as e:
            self.logger.error(f"error when read file {filename} with exception {e}")
            self.logger.debug('using default program input (-s | --stringProgram)')
            return program_input_default

    def write_output_file(self, eval_fn: Callable[[], None]):
        filename = self.program_output_filename
        try:
            with open(filename, 'w') as file:
                sys.stdout = file
                eval_fn()
            sys.stdout = sys.__stdout__
        except Exception as e:
            sys.stdout = sys.__stdout__
            os.remove(filename)
            self.logger.error(f"error when write output file {filename} with exception {e}")

    def tokenize(self, program_input):
        tokens = get_all_tokens(Lexer().build(), program_input)
        label = 'Lexer Tokens'
        self.__log_wrapper_if(
            self.is_show_tokenize,
            label,
            label,
            lambda: self.logger.print(tokens)
        )
        return tokens

    def show_program_input(self, _program_input):
        is_empty_program = _program_input == ""
        label = 'Program Input'
        self.__log_wrapper_if(
            self.is_show_program_input or is_empty_program,
            label,
            label,
            lambda: self.logger.print(_program_input) if not is_empty_program else self.logger.warn('Empty program!!')
        )

    def show_parser_ast(self, ast):
        label = 'AST Parsed'
        self.__log_wrapper_if(
            self.is_show_parser_ast,
            label,
            label,
            lambda: self.logger.print(f"{ast}")
        )

    # show
    def __log_wrapper_if(self, show: bool, header_str: str, footer_str: str, fn: Callable[[], None]):
        if show:
            self.logger.print(f"{{ {header_str} }} => \n")
            fn()
            self.logger.print(f"\n{{ END {footer_str} }}\n")
