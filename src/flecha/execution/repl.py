from flecha.interpreter.environment import LocalEnvironment
from flecha.interpreter.package import Interpreter
from flecha.parser import Parser

class REPL:
    def __init__(self):
        self.parser = Parser()
        self.intpr = Interpreter()

    def run(self):
        self.parser.greet()
        print("write 'exit' for quit")
        is_exit = False
        env = LocalEnvironment()
        while not is_exit:
            fl_source = input('> ')
            match fl_source:
                case 'exit':
                    is_exit = True
                case _ if fl_source.lstrip() != "":
                    self.parse_and_eval(fl_source, env)

    def parse_and_eval(self, fl_source, env):
        try:
            ast = self.parser.parse(f'def main = {fl_source}')
            print(self.intpr.eval(ast, env))
        except Exception as e:
            print(f'ERROR | {e}')
