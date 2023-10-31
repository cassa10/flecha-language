from flecha.ast_impl.ast_node import AstNode
from flecha.ast_impl.label import AstLabel
from flecha.interpreter.values import *

MAIN_DEF = 'main'

UNSAFE_PRINT_INT = 'unsafePrintInt'
UNSAFE_PRINT_CHAR = 'unsafePrintChar'
UNARY_NOT = '!'
UNARY_MINUS = '-'


class GlobalEnvironment:
    def __init__(self):
        self.globals = {}

    def extend(self, _id, val):
        self.globals[_id] = val

    def lookup(self, _id):
        try:
            return self.globals[_id]
        except:
            raise RuntimeError(f'Id {_id} not defined')


class LocalEnvironment:

    def __init__(self):
        self.stack_frame = []

    def extend(self, _id, val):
        self.stack_frame = [(_id, val)] + self.stack_frame

    def lookup(self, _id1):
        return next((val for _id2, val in self.stack_frame if _id2 == _id1), None)


class Interpreter:

    def __init__(self):
        self.global_env = GlobalEnvironment()
        self.eval_mapper = {
            AstLabel.Program: self.eval_program,
            AstLabel.Def: self.eval_def,
            AstLabel.ExprApply: self.eval_apply,
            AstLabel.ExprVar: self.eval_var,
            AstLabel.ExprChar: self.eval_char,
            AstLabel.ExprNumber: self.eval_number,
        }

        self.eval_unary = {
            UNSAFE_PRINT_INT: self.eval_print_int,
            UNSAFE_PRINT_CHAR: self.eval_print_char,
            UNARY_NOT: self.eval_not,
            UNARY_MINUS: self.eval_uminus,
        }

    def eval(self, ast: AstNode, env=LocalEnvironment()):
        try:
            return self.eval_mapper[ast.label](ast, env)
        except:
            raise RuntimeError(f'Eval Error: invalid ast {ast}')

    def eval_program(self, ast, env):
        for _def in ast.get_defs():
            self.eval_def(_def, env)
        return self.global_env.lookup(MAIN_DEF)

    def eval_def(self, ast, env):
        self.global_env.extend(ast.id(), self.eval(ast.expr(), env))
        return VoidValue()

    def eval_apply(self, ast, env):
        func = ast.func()
        unary_op = func.id().value
        return self.eval_unary[unary_op](ast.arg(), env)

    def eval_var(self, ast, env):
        return self.find_in_envs(ast.id(), env)

    def eval_char(self, ast):
        return CharValue(ast.value)

    def eval_number(self, ast):
        return IntValue(ast.value)

    def eval_print_int(self, ast, _):
        self.print(self.eval_number(ast))
        return VoidValue()

    def eval_print_char(self, ast, _):
        self.print(self.eval_char(ast))
        return VoidValue()

    def eval_not(self, ast, env):
        pass

    def eval_uminus(self, ast, env):
        pass

    def print(self, value):
        print(value, end='')

    def find_in_envs(self, _id, env):
        value = env.lookup(_id)
        return value if value else self.global_env.lookup(_id)
