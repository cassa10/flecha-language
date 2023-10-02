import argparse

from flecha.lexer import get_all_tokens, Lexer
from flecha.parser import Parser


def get_or_default(atr, default):
    if atr in (None, '', ' '):
        return default
    return atr


def get_main_args(arg_parser):
    # Inputs and outputs
    arg_parser.add_argument("-s", "--stringProgram", help="some valid string program")
    arg_parser.add_argument("-i", "--inputFile", help="path to input file with program")
    # argParser.add_argument("-o", "--outputFile", help="path to object output file")

    # Mode Tokenizer
    arg_parser.add_argument("-t", "--tokenize", help="Mode tokenize program input")

    args = arg_parser.parse_args()
    print("args=%s" % args)

    print("args.name=%s" % args.stringProgram)
    return (get_or_default(args.stringProgram, ''), get_or_default(args.tokenize, False),
            get_or_default(args.inputFile, ''), get_or_default(args.stringProgram, ''))


def main(program_input):
    parser = Parser()
    print(parser)
    #print(program_input)
    print("lexer =>")
    print(get_all_tokens(Lexer().build(), program_input))
    print("parser=>")
    print(f"{parser.parse(program_input)}")


if __name__ == "__main__":
    #_argParser = argparse.ArgumentParser()
    #program, tokenize_mode, input_file, output_file = get_main_args(_argParser)
    program = "def tres = \\\\1\t\n+2 \n --hola"
    main(program)
