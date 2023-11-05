
def get_or_default(atr, default):
    atr_striped = atr.strip() if issubclass(type(atr), str) else atr
    if atr_striped in (None, ''):
        return default
    return atr


class Config:

    def __init__(self, arg_parser):
        self.arg_parser = arg_parser

        args = self.load()

        if args.debug:
            print(f"Arguments: {args}")

        self.show_parser_ast = args.parse
        self.show_tokens = args.tokenize
        self.debug_mode = args.debug
        self.program_from_str = get_or_default(args.stringProgram, '')
        self.program_from_file = get_or_default(args.inputFile, '')
        self.output_file = get_or_default(args.outputFile, '')
        self.run_repl = args.repl

    def load(self):

        self.arg_parser.add_argument("-r", "--repl", action='store_true', help="use flecha REPL (Priority 1)")

        # Inputs
        self.arg_parser.add_argument("-s", "--stringProgram", help="some valid string program")
        self.arg_parser.add_argument("-i", "--inputFile", help="path to input file with program")

        # Outputs
        self.arg_parser.add_argument("-o", "--outputFile", help="path to object output file")

        # Mode Tokenizer
        self.arg_parser.add_argument("-t", "--tokenize", action='store_true',
                                     help="Show tokenize returning tokens of the program input")
        self.arg_parser.add_argument("-tM", "--tokenizeMode", action='store_false',
                                     help="Mode tokenize only returning tokens of the program input (Priority 2)")

        # Mode Parser
        self.arg_parser.add_argument("-p", "--parse", action='store_true',
                                     help="Show parser returning AST of the program input")
        self.arg_parser.add_argument("-pM", "--parseMode", action='store_false',
                                     help="Mode parser returning only AST of the program input (Priority 3)")

        # Debug
        self.arg_parser.add_argument("-d", "--debug", action='store_true',
                                     help="Mode debug for watch program input and some debugging info")

        return self.arg_parser.parse_args()
