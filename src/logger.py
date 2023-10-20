
class Logger:

    def __init__(self, debug_mode: bool):
        self.debug_mode = debug_mode

    def debug(self, msg):
        if self.debug_mode:
            self.print_level('DEBUG', msg)

    def info(self, msg):
        self.print_level('INFO', msg)

    def warn(self, msg):
        self.print_level('WARN', msg)

    def error(self, msg):
        self.print_level('ERROR', msg)

    def print(self, msg):
        print(msg)

    def print_level(self, level, msg):
        print(f"{level} | {msg}")
