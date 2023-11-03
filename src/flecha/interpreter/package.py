from flecha.ast_impl.expression import *
from flecha.ast_impl.label import AstLabel
from flecha.interpreter.environment import *
from flecha.interpreter.values import *


def type_runtime_exception(_type, val):
    return RuntimeError(f'Eval Error | {val} is not {_type.value}')


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
            AstLabel.ExprLet: self.eval_let,
            AstLabel.ExprLambda: self.eval_lambda,
            AstLabel.ExprConstructor: self.eval_constructor,
            AstLabel.ExprCase: self.eval_case,
        }

        self.eval_unary = {
            UNSAFE_PRINT_INT: self.eval_print_int,
            UNSAFE_PRINT_CHAR: self.eval_print_char,
            UNARY_NOT: self.eval_not,
            UNARY_MINUS: self.eval_uminus,
        }

        self.eval_binary_bool = {
            BINARY_EQ: lambda x, y: x == y,
            BINARY_NE: lambda x, y: x != y,
            BINARY_GE: lambda x, y: x >= y,
            BINARY_LE: lambda x, y: x <= y,
            BINARY_GT: lambda x, y: x > y,
            BINARY_LT: lambda x, y: x < y,
        }

        self.eval_binary_arithmetic = {
            BINARY_ADD: lambda x, y: x + y,
            BINARY_SUB: lambda x, y: x - y,
            BINARY_MUL: lambda x, y: x * y,
            BINARY_DIV: lambda x, y: x / y,
            BINARY_MOD: lambda x, y: x % y,
        }

        self.eval_binary_logical = {
            BINARY_OR: lambda x, y: self.eval_or,
            BINARY_AND: lambda x, y: self.eval_and,
        }


    def eval(self, ast: AstNode, env=LocalEnvironment()):
        try:
            # noinspection PyArgumentList
            return self.eval_mapper[ast.label](ast, env)
        except KeyError:
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
        arg = ast.arg()
        if func.label == AstLabel.ExprVar and func.id() in self.eval_unary:
            return self.eval_unary[func.id()](arg, env)

        #func_prime = func.func()
        #if func_prime == AstLabel.ExprVar and func_prime.id() in operators[OP_BINARY]:

        if self.is_struct(func):
            return self.eval_struct(func, arg, env)

        arg_eval = self.eval(ast.arg(), env)
        closure_eval = self.eval_closure(func, env)
        return self.eval(closure_eval.body, closure_eval.extend_env(closure_eval.param, arg_eval))

    def eval_constructor(self, ast, _):
        return StructValue(ast.id(),[])

    def eval_struct(self, func, arg, env):
        func_i = func
        evaluated_args = [self.eval(arg, env)]
        while func_i.label == AstLabel.ExprApply:
            evaluated_args = [self.eval(func_i.arg(), env)] + evaluated_args
            func_i = func.func()
        return StructValue(func_i.id(), evaluated_args)

    def is_struct(self, func):
        if func == AstLabel.ExprApply:
            return False or self.is_struct(func.func())
        return func.label == AstLabel.ExprConstructor

    def eval_closure(self, ast, env):
        val = self.eval(ast, env)
        if not val.is_closure():
            raise type_runtime_exception(Types.Closure, val)
        return val

    def eval_unary(self, ast, env):
        func = ast.func()
        operation = func.id()
        return self.eval_unary[operation](ast.arg(), env)

    def eval_binary(self, ast, env):
        pass

    def eval_var(self, ast, env):
        return self.find_in_envs(ast.id(), env)

    def eval_char(self, ast, _):
        return CharValue(ast.value)

    def eval_number(self, ast, _):
        return IntValue(ast.value)

    def eval_print_int(self, ast, env):
        number = self.eval(ast, env)
        if not number.is_int():
            raise type_runtime_exception(Types.Int, number)
        self.print(number)
        return VoidValue()

    def eval_print_char(self, ast, env):
        char = self.eval(ast, env)
        if not char.is_char():
            raise type_runtime_exception(Types.Char, char)
        self.print(char)
        return VoidValue()

    def eval_not(self, ast, env):
        pass

    def eval_uminus(self, ast, env):
        pass

    def eval_let(self, ast, env):
        let_val = self.eval(ast.arg(), env)
        return self.eval(ast.expr_in(), env.extend(ast.param(), let_val))

    def eval_lambda(self, ast, env):
        return ClosureValue(ast.param(), ast.expr(), env)

    def eval_case(self, ast, env):
        value = self.eval(ast.expr(), env)
        for branch in ast.branches():
            is_matched, env_extended = self.case_match(value, branch, env)
            if is_matched:
                return self.eval(branch.expr(), env_extended)
        raise RuntimeError(f'Could not match {value}!')

    def case_match(self, case_val, branch_to_match, env):
        if case_val.is_struct():
            return self.struct_match(case_val, branch_to_match, env)
        return case_val.type == branch_to_match.id(), env

    def struct_match(self, case_val, branch_to_match, env):
        env_prime = env
        match_id = case_val.constructor == branch_to_match.id()
        match_args_len = case_val.args_len() == len(branch_to_match.params())
        full_matched = match_id and match_args_len
        if full_matched:
            for i, param in enumerate(branch_to_match.params()):
                env_prime = env_prime.extend(param, case_val.get_arg(i))
            return full_matched, env_prime
        return full_matched, env_prime



    def print(self, value):
        print(value, end='')

    def find_in_envs(self, _id, env):
        value = env.lookup(_id)
        return value if value else self.global_env.lookup(_id)
