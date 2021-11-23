from part1 import *
from part2 import *

import math
import time

def dcsolve(operators, constants, input_outputs):
    """
    operators: list of classes, such as [Times, Not, ...]. Note that `If` does not have to be here, because the decision tree learner inserts such expressions
    constants: list of possible leaves in syntax tree, such as [Number(1)]. Variables can also be leaves, but these are automatically inferred from `input_outputs`
    input_outputs: list of tuples of environment (the input) and desired output, such as [({'x': 5}, 6), ({'x': 1}, 2)]
    returns: an expression `p` which should satisfy `all( p.evaluate(input) == output for input, output in input_outputs )`
    """
    # separate bools and ints
    ints = set()
    cover = {}
    preds = set()
    for expression in bottom_up_generator(3, operators, constants, input_outputs):
        outputs = tuple(expression.evaluate(input) for input, _ in input_outputs)
        if expression.return_type == "int":
            bool_tuple = tuple(outputs[i] == input_outputs[i][1] for i in range(len(input_outputs)) )
            ints.add(expression)
            cover[expression] = bool_tuple
        elif expression.return_type == "bool":
            preds.add((expression, outputs))
    
    examples_we_care_about = [i for i in range(len(input_outputs))]
    return learn_decision_tree(cover, ints, preds, examples_we_care_about)

def learn_decision_tree(cover, terms, predicates, examples_we_care_about):
    """
    You may find this utility function helpful
    cover: dictionary mapping from expression to tuple of bool's. `cover[e][i] == True` iff expression `e` predicts the correct output for `i`th input
    terms: set of expressions that we can use as leaves in the decision tree
    predicates: predicates we can use as branches in the decision tree. each element of `predicates` should be a tuple of `(expression, outputs)` where `outputs` is a tuple of bool's. Should satisfy `outputs[i] == expression.evaluate(input_outputs[i][0])`
    examples_we_care_about: a set of integers, telling which input outputs we care about solving for. For example if we are done, then this will be the empty set. If we are just starting out synthesizing the decision tree, then this will be the numbers 0-(len(input_outputs)-1)
    """

    for expression in terms:
        if all( cover[expression][i] for i in examples_we_care_about ):
            return expression

    if len(predicates) == 0: return None # no more predicates to split on

    def information_gain(predicate_info):
        """actually returns -information gain up to a constant ($G$ in paper)"""
        predicate, predicate_outputs = predicate_info

        examples_yes = {i for i in examples_we_care_about if predicate_outputs[i] }
        examples_no = {i for i in examples_we_care_about if not predicate_outputs[i] }
        
        probability_yes = len(examples_yes)/len(examples_we_care_about)
        probability_no = len(examples_no)/len(examples_we_care_about)
        
        entropy_yes = entropy(examples_yes)
        entropy_no = entropy(examples_no)

        return probability_yes * entropy_yes + probability_no * entropy_no

    def entropy(example_indices):
        # entries proportional probability that the term used during evaluation is a specific term
        # len of `distribution` will be the number of terms
        distribution = []

        for expression in terms:
            # calculate probability that we used this expression, assuming uniform distribution over which example is being run
            ps = []
            for example_index in example_indices:
                if not cover[expression][example_index]: # we can't explain this example, definitely are not a candidate term
                    p = 0
                else:
                    p = sum( cover[expression][i] for i in example_indices )
                    p /= sum( cover[other_expression][i]
                              for other_expression in terms
                              if cover[other_expression][example_index]
                              for i in example_indices)
                ps.append(p)
            
            distribution.append(sum(ps))

        # original paper has 1/|pts| term, but we can absorb this into normalizing constant
        z = sum(distribution) # normalizing constant

        return -sum( p/z * math.log(p/z) for p in distribution if p > 0)
        
    predicate, predicate_outputs = min(predicates, key=information_gain)

    left_hand_side_examples = {i for i in examples_we_care_about if predicate_outputs[i]}
    right_hand_side_examples = {i for i in examples_we_care_about if not predicate_outputs[i]}

    predicates = predicates - {(predicate, predicate_outputs)}

    lhs = learn_decision_tree(cover, terms, predicates, left_hand_side_examples)
    if lhs is None: return None
    
    rhs = learn_decision_tree(cover, terms, predicates, right_hand_side_examples)
    if rhs is None: return None

    return If(predicate, lhs, rhs)

    
    
def test_dcsolve():
    operators = [Plus,Times,LessThan,And,Not]
    terminals = [FALSE(),Number(0),Number(1),Number(-1)]

    # collection of input-output specifications
    test_cases = []
    test_cases.append([({"x": 1}, 1),
                       ({"x": 4}, 16),
                       ({"x": 5}, 25)])
    test_cases.append([({"x": 1, "y": 2}, 1),
                       ({"x": 5, "y": 2}, 2),
                       ({"x": 99, "y": 98}, 98),
                       ({"x": 97, "y": 98}, 97),])
    test_cases.append([({'x':10, 'y':7}, 17),
	                    ({'x':4, 'y':7}, -7),
	                    ({'x':10, 'y':3}, 13),
	                    ({'x':1, 'y':-7}, -6),
	                    ({'x':1, 'y':8}, -8)])
    test_cases.append([({'x':10, 'y':10}, 20),
                       ({'x':15, 'y':15}, 30),
	               ({'x':4, 'y':7}, 16),
	               ({'x':10, 'y':3}, 9),
	               ({'x':1, 'y':-7}, 49),
	               ({'x':1, 'y':8}, 1)])

    for test_case in test_cases:
        start_time = time.time()
        expression = dcsolve(operators, terminals, test_case)
        print(f"synthesized program:\n{expression.pretty_print(0, True, True)} in {time.time() - start_time} seconds")
        for xs, y in test_case:
            assert expression.evaluate(xs) == y, f"synthesized program {expression.pretty_print()} does not satisfy the following test case: {xs} --> {y}"
            print(f"passes test case {xs} --> {y}")

        print()

    print(" [+] dcsolver passes tests")


if __name__ == "__main__":
    test_dcsolve()
