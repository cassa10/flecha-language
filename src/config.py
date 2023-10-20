
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

        self.parser_mode = args.parse
        self.tokenize_mode = args.tokenize
        self.debug_mode = args.debug
        self.program_from_str = get_or_default(args.stringProgram, '')
        self.program_from_file = get_or_default(args.inputFile, '')

    def load(self):
        # Inputs and outputs
        self.arg_parser.add_argument("-s", "--stringProgram", help="some valid string program")
        self.arg_parser.add_argument("-i", "--inputFile", help="path to input file with program")

        # TODO: generate output file
        #  argParser.add_argument("-o", "--outputFile", help="path to object output file")

        # Mode Parser
        self.arg_parser.add_argument("-p", "--parse", action='store_true',
                                     help="Mode parser returning AST of the program input")
        # Mode Tokenizer
        self.arg_parser.add_argument("-t", "--tokenize", action='store_true',
                                     help="Mode tokenize returning tokens of the program input")

        # Debug
        self.arg_parser.add_argument("-d", "--debug", action='store_true',
                                     help="Mode debug for watch program input and some debugging info")

        return self.arg_parser.parse_args()
