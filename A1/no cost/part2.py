from part1 import *

from collections import defaultdict
import itertools
import time
from frozendict import frozendict


def bottom_up(global_bound, operators, constants, input_outputs):
    """
    global_bound: int. an upper bound on the size of expression
    operators: list of classes, such as [Times, If, ...]
    constants: list of possible leaves in syntax tree, such as [Number(1)]. Variables can also be leaves, but these are automatically inferred from `input_outputs`
    input_outputs: list of tuples of environment (the input) and desired output, such as [({'x': 5}, 6), ({'x': 1}, 2)]
    returns: either None if no program can be found that satisfies the input outputs, or the smallest such program. If a program `p` is returned, it should satisfy `all( p.evaluate(input) == output for input, output in input_outputs )`
    """

    target_outputs = tuple(y for x, y in input_outputs)

    for expression in bottom_up_generator(global_bound, operators, constants, input_outputs):
        outputs = tuple(expression.evaluate(input)
                        for input, output in input_outputs)

        if outputs == target_outputs:
            return expression

    return None


def bottom_up_generator(global_bound, operators, constants, input_outputs):
    """
    global_bound: int. an upper bound on the size of expression
    operators: list of classes, such as [Times, If, ...]
    constants: list of possible leaves in syntax tree, such as [Number(1)]. Variables can also be leaves, but these are automatically inferred from `input_outputs`
    input_outputs: list of tuples of environment (the input) and desired output, such as [({'x': 5}, 6), ({'x': 1}, 2)]
    yields: sequence of programs, ordered by expression size, which are semantically distinct on the input examples
    """
    def number_of_correct_input_outputs(evaluated_val_in_envs):
        return sum(evaluated_val_in_envs[frozendict(input)] == output for input, output in input_outputs)

    def evaluate_val_in_envs(exp):
        return frozendict({frozendict(env): exp.evaluate(env) for env, _ in input_outputs})

    # suggested first thing: variables and constants should be treated the same, because they are both leaves in syntax trees
    # after computing `variables_and_constants`, you should no longer refer to `constants`. express everything in terms of `variables_and_constants`
    # `make_variable` is just a helper function for making variables that smartly wraps the variable name in the correct class depending on the type of the variable
    def make_variable(variable_name, variable_value):
        from part4 import StringVariable
        if isinstance(variable_value, int):
            return NumberVariable(variable_name)
        if isinstance(variable_value, str):
            return StringVariable(variable_name)
        assert False, "only numbers and strings are supported as variable inputs"
    variables = list({make_variable(variable_name, variable_value)
                      for inputs, outputs in input_outputs
                      for variable_name, variable_value in inputs.items()})
    variables_and_constants = constants + variables

    # suggested data structure (you don't have to use this if you don't want):
    # a mapping from a tuple of (type, expression_size) to all of the possible values that can be computed of that type using an expression of that size
    organized_exps = defaultdict(lambda: set())
    evaluated_vals = set()

    # add variables & constants
    for var_or_const in variables_and_constants:
        organized_exps[(var_or_const.return_type, 1)].add(var_or_const)
        evaluated_val = evaluate_val_in_envs(var_or_const)
        if evaluated_val not in evaluated_vals:
            evaluated_vals.add(evaluated_val)
            yield var_or_const

    prog_len = 2
    while prog_len <= global_bound:
        for op in operators:
            arg_typs = op.argument_types
            num_args = len(arg_typs)
            if len(arg_typs) != 0:
                all_partitions = integer_partitions(
                prog_len-1, num_args)
                all_partitions = list(filter(lambda x: x.count(0) == 0, all_partitions))
                for partition in all_partitions:
                    prev_exps = []
                    for i in range(num_args):
                        typ = arg_typs[i]
                        exp_size = partition[i]
                        prev_exps.append(organized_exps[(typ, exp_size)])

                    # perform operations w/ args
                    for args in itertools.product(*prev_exps):
                        new_exp = op(*args)
                        # map {map(env):evaluated expression}
                        evaluated_val_in_envs = evaluate_val_in_envs(new_exp)
                        correct_envs = set(frozendict(input) for input, output in input_outputs if new_exp.evaluate(input) == output)
                        if evaluated_val_in_envs not in evaluated_vals:
                            evaluated_vals.add(evaluated_val_in_envs)
                            if len(input_outputs) > 2:
                                if prog_len <= 3 or len(correct_envs) >= 3:                            
                                    organized_exps[(new_exp.return_type, prog_len)].add(
                                        new_exp)
                                    yield new_exp
                            else:
                                organized_exps[(new_exp.return_type, prog_len)].add(
                                        new_exp)
                                yield new_exp

                        
                            
                
        prog_len += 1


def integer_partitions(target_value, number_of_arguments):
    """
    Returns all ways of summing up to `target_value` by adding `number_of_arguments` nonnegative integers
    You may find this useful when implementing `bottom_up_generator`:

    Imagine that you are trying to enumerate all expressions of size 10, and you are considering using an operator with 3 arguments.
    So the total size has to be 10, which includes +1 from this operator, as well as 3 other terms from the 3 arguments, which together have to sum to 10.
    Therefore: 10 = 1 + size_of_first_argument + size_of_second_argument + size_of_third_argument
    Also, every argument has to be of size at least one, because you can't have a syntax tree of size 0
    Therefore: 10 = 1 + (1 + size_of_first_argument_minus_one) + (1 + size_of_second_argument_minus_one) + (1 + size_of_third_argument_minus_one)
    So, by algebra:
         10 - 1 - 3 = size_of_first_argument_minus_one + size_of_second_argument_minus_one + size_of_third_argument_minus_one
    where: size_of_first_argument_minus_one >= 0
           size_of_second_argument_minus_one >= 0
           size_of_third_argument_minus_one >= 0
    Therefore: the set of allowed assignments to {size_of_first_argument_minus_one,size_of_second_argument_minus_one,size_of_third_argument_minus_one} is just the integer partitions of (10 - 1 - 3).
    """

    if target_value < 0:
        return []

    if number_of_arguments == 1:
        return [[target_value]]

    return [[x1] + x2s
            for x1 in range(target_value + 1)
            for x2s in integer_partitions(target_value - x1, number_of_arguments - 1)]


def test_bottom_up():
    operators = [Plus, Times, LessThan, And, Not, If]
    terminals = [FALSE(), Number(0), Number(1), Number(-1)]

    # collection of input-output specifications
    test_cases = []
    test_cases.append([({"x": 1}, 1),
                       ({"x": 4}, 16),
                       ({"x": 5}, 25)])
    test_cases.append([({"x": 1, "y": 2}, 1),
                       ({"x": 5, "y": 2}, 2),
                       ({"x": 99, "y": 98}, 98),
                       ({"x": 97, "y": 98}, 97), ])
    test_cases.append([({'x': 10, 'y': 7}, 17),
                       ({'x': 4, 'y': 7}, -7),
                       ({'x': 10, 'y': 3}, 13),
                       ({'x': 1, 'y': -7}, -6),
                       ({'x': 1, 'y': 8}, -8)])
    test_cases.append([({'x': 10, 'y': 10}, 20),
                       ({'x': 15, 'y': 15}, 30),
                       ({'x': 4, 'y': 7}, 16),
                       ({'x': 10, 'y': 3}, 9),
                       ({'x': 1, 'y': -7}, 49),
                       ({'x': 1, 'y': 8}, 1)])

    # the optimal size of each program that solves the corresponding test case
    optimal_sizes = [3, 6, 10, 17]

    for test_case, optimal_size in zip(test_cases, optimal_sizes):
        assert bottom_up(optimal_size - 1, operators, terminals,
                         test_case) is None, f"you should not be able to solve this test case w/ a program whose syntax tree is of size {optimal_size-1}. the specific test case is {test_case}"

        start_time = time.time()
        expression = bottom_up(optimal_size, operators, terminals, test_case)
        assert expression is not None, f"failed to synthesize a program when the size bound was {optimal_size}. the specific test case is {test_case}"

        print(
            f"synthesized program:\n{expression.pretty_print(0, True, True)} in {time.time() - start_time} seconds")
        for xs, y in test_case:
            assert expression.evaluate(
                xs) == y, f"synthesized program {expression.pretty_print()} does not satisfy the following test case: {xs} --> {y}"
            print(f"passes test case {xs} --> {y}")

        print()

    print(" [+] bottom-up synthesis passes tests")


if __name__ == "__main__":
    test_bottom_up()
