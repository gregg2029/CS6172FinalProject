from part1 import *
from part2 import *
from part3 import *

import re
import time
import frozendict

class Concatenate(Expression):
    return_type = "str"
    argument_types = ["str", "str"]
    
    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return f"Concatenate({self.left}, {self.right})"

    def pretty_print(self):
        return f'{self.left.pretty_print()} + {self.right.pretty_print()}'

    def evaluate(self, environment):
        return self.left.evaluate(environment) + self.right.evaluate(environment)

    def extension(self):
        return [Concatenate(left, right)
                for left in self.left.extension()
                for right in self.right.extension() ]

    def arguments(self):
        return [self.left, self.right]
    
    def version_space_size(self):
        return self.left.version_space_size() * self.right.version_space_size()
    
    def minimum_cost_member_of_extension(self):
        return Concatenate(self.left.minimum_cost_member_of_extension(), self.right.minimum_cost_member_of_extension())

class ConstantString(Expression):
    return_type = "str"
    argument_types = []
    
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f'ConstantString("{self.content}")'

    def pretty_print(self):
        return f'"{self.content}"'

    def evaluate(self, environment):
        return self.content

    def arguments(self):
        return []
    
    def version_space_size(self):
        return 1
    
    def extension(self):
        return [self]
    
    def minimum_cost_member_of_extension(self):
        return self
    
    def cost(self):
        if self.content == ',' or self.content == ' ' or self.content == '.':
            return 1
        return 20 + len(self.content)




class Substring(Expression):
    return_type = "str"
    argument_types = ["str", "int", "int"]
    
    def __init__(self, the_string, left, right):
        self.the_string, self.left, self.right = the_string, left, right

    def __str__(self):
        return f'Substring({self.the_string}, {self.left}, {self.right})'

    def pretty_print(self):
        return f'Substring({self.the_string.pretty_print()}, {self.left.pretty_print()}, {self.right.pretty_print()})'

    def evaluate(self, environment):
        """
        Slightly different semantics from ordinary python list slicing:
        We think of the indices as referring to characters in the string, rather than referring to places in between characters
        The extracted substring is the span between the start and end indices, **inclusive** (so it includes the ending index)
        This causes the start and end indices to be treated symmetrically - specifically both `the_string[left]` and `the_string[right]` will be in the output
        If an index is negative, we make it positive by calculating `len(the_string) + the_index`
        As a consequence, `Substring(string, 0, -1)` gives the entire string.
        """
        the_string = self.the_string.evaluate(environment)
        left = self.left.evaluate(environment)
        right = self.right.evaluate(environment)

        # if the index = -1, that refers to the last character
        if left < 0: left = len(the_string) + left
        if right < 0: right = len(the_string) + right
        
        return the_string[left : right + 1]

    def extension(self):
        return [Substring(s,l,r)
                for s in self.the_string.extension()
                for l in self.left.extension()
                for r in self.right.extension() ]

    def arguments(self):
        return [self.the_string, self.left, self.right]
    
    def version_space_size(self):
        return self.the_string.version_space_size() * self.left.version_space_size() * self.right.version_space_size()
    
    def minimum_cost_member_of_extension(self):
        return Substring(self.the_string.minimum_cost_member_of_extension(), self.left.minimum_cost_member_of_extension(), self.right.minimum_cost_member_of_extension())

    




class StringVariable(Expression):
    return_type = "str"
    argument_types = []
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"StringVariable('{self.name}')"

    def pretty_print(self):
        return self.name

    def evaluate(self, environment):
        return environment[self.name]

    def extension(self):
        return [self]

    def version_space_size(self): return 1

    def arguments(self):
        return []
    
    def version_space_size(self):
        return 1
    
    def minimum_cost_member_of_extension(self):
        return self
    
    def cost(self):
        return 1


def test_evaluation():
    x = "(555) 993-4777"
    y = "993"
    assert Substring(StringVariable('x'),
                     Number(6),
                     Number(8)).evaluate({'x': x}) == y

    assert Substring(StringVariable('x'),
                     Number(-8),
                     Number(8)).evaluate({'x': x}) == y

    assert Substring(StringVariable('x'),
                     Number(6),
                     Number(-6)).evaluate({'x': x}) == y

    assert Substring(StringVariable('x'),
                     Number(-8),
                     Number(-6)).evaluate({'x': x}) == y

    print(" [+] text editing evaluation passes checks")

if __name__ == "__main__":
    test_evaluation()

class Union(Expression):
    def __init__(self, members):
        self.members = members

    def __str__(self):
        return 'Union(' + ', '.join([str(m) for m in self.members ]) + ')'

    def pretty_print(self):
        return 'Union(' + ', '.join([m.pretty_print() for m in self.members ]) + ')'

    def extension(self):
        return [ expression
                 for member in self.members
                 for expression in member.extension() ]

    def evaluate(self, environment):
        assert False, "cannot evaluate union"

    @staticmethod
    def make(members):
        """
        Helper function for building unions
        Flattens nested unions, and prevents the creation of singleton unions
        """
        members = [ expression
                    for member in members
                    for expression in (member.members if isinstance(member, Union) else [member]) ]
        if len(members) == 1: return members[0]
        return Union(members)

    def minimum_cost_member_of_extension(self):
        return min([ member.minimum_cost_member_of_extension() for member in self.members ],
                   key=lambda expression: expression.cost())

    def version_space_size(self):
        return sum( member.version_space_size() for member in self.members )


def test_version_spaces():
    v = Union([Substring(StringVariable('x'),
                        Union([Number(2), Number(1)]),
                        Union([Number(-2), Number(-1)])),
               ConstantString("hello world")])
    assert v.version_space_size() == 5, "problem with version_space_size"
    assert len(v.extension()) == 5, "problem with extension"

    v = Union([Concatenate(v,v), StringVariable('y')])
    assert str(v.minimum_cost_member_of_extension()) == "StringVariable('y')", "problem with `minimum_cost_member_of_extension`"
    print(" [+] version space evaluation passes checks")

if __name__ == "__main__":
    test_version_spaces()

def generate_substring(environment, target_output):
    """
    environment: a dictionary mapping a variable name to a value. Both names and values are strings
    target_output: the target output of the `Substring` program when run on `environment`
    returns: a version space containing all Substring operators which can map the `environment` to the `target_output`
    """
    result = set()
    result.add(ConstantString(target_output))
    for key, value in environment.items():
        pattern = re.escape(target_output)
        for match in re.finditer(pattern, value):
            k = match.start()
            end = match.end()
            y_1 = generate_position(value, k)
            y_2 = generate_position(value, end-1)
            result.add(Substring(StringVariable(key), y_1, y_2))
    return Union(result)

def generate_position(string, i):
    """
    string: a string that was provided as an input in the specification
    i: an index of a character in that string
    returns: a version space of programs which will index that character"""
    len_of_string = len(string)
    return Union.make((Number(i), Number(-(len_of_string-i))))

def extra_credit_witness_synthesize(specification, components,
                                    dynamic_programming_table=None):
    """
    specification: a spec on what the target program should be
                   such specifications are either a single program, i.e. an `Expression`, meaning that the specified program has to be that exact expression
                   OR, a specification is a tuple of (input, target_output)
    
    components: a list of classes, such as `Number`, `Concatenate`, ...
                these classes must implement a static method called `witness`
                `witness` takes as input a specification and returns a disjunction of conjunctions of specification on the arguments to the constructor class of a DSL component.
                Disjunctions and conjunctions are represented as lists.
                For example, given class `K` for a DSL component w/ arity 2, if the return value of `K.witness(spec)` is of the form:
                    [ [spec_1_1,spec_1_2], [spec_2_1,spec_2_2], [spec_3_1,spec_3_2]]
                this means that `K(expr_i_1, expr_i_2)` satisfies `spec` whenever `expr_i_1` satisfies `spec_i_1` and `expr_i_2` satisfies `spec_i_2`, where i=1..3

    For example, you could define `Concatenate.witness` as:
```
    @staticmethod
    def witness(specification):
        environment, target_output = specification # unpack the spec
        if not isinstance(target_output, str): # `Concatenate` can only make string outputs
            return [] # empty disjunction - i.e. impossible/false/bottom

        possibilities = [] # a disjunction of different possible ways of concatenating to make output
        for size_of_prefix in range(1, len(target_output)):
            prefix = target_output[:size_of_prefix]
            suffix = target_output[size_of_prefix:]
            assert target_output == prefix + suffix

            possibilities.append([[environment, prefix], # spec on prefix...
                                  [environment, suffix]]) # ...conjount w/ spec on suffix

        return possibilities # returning a (list of) disjunctions, each of which is a (list of) conjunctions
```

    In order to handle constant constructors `K`, such as `Number` and `ConstantString`, we recommend also allowing `witness` to just return an entire instance of type `K` rather than return conjunctions of specs.
    
    For example, you could define `ConstantString.witness` as:
```
     @staticmethod
     def witness(specification):
         inputs, target_output = specification
         if isinstance(target_output, str):
             return [ConstantString(target_output)]
         else:
             return []
```
    """
    assert False, "implement as part of extra credit (OPTIONAL)"

    

def flashfill_one_example(environment, target_output,
                          dynamic_programming_table=None):
    """
    environment: a dictionary mapping a variable name to a value. Both names and values are strings
    target_output: the target output of the program when run on `environment`
    """

    if dynamic_programming_table is None:
        dynamic_programming_table = {}

    # this allows you to use the `environment` as a key in a dictionary for dynamic programming
    # this is because the dictionary is a hash table,
    # and you cannot hash mutable objects
    # so this "freezes" the dictionary, making it immutable, and hence something you can hash
    environment = frozendict.frozendict(environment)
    key = (environment, target_output)
    if key in dynamic_programming_table:
        return dynamic_programming_table[key]

    spaces = set()
    spaces.add(generate_substring(*key))
    for i in range(1, len(target_output)):
        vs_left = flashfill_one_example(environment, target_output[:i], dynamic_programming_table)
        vs_right = flashfill_one_example(environment, target_output[i:], dynamic_programming_table)
        spaces.add(Concatenate(vs_left, vs_right))
    union = Union.make(spaces)
    dynamic_programming_table[key] = union
    return union

def intersect_args(elem1, elem2, dynamic_programming_table=None):
    arg_intersections = []
    for arg_index in range(len(elem1.arguments())):
        elem1_arg = elem1.arguments()[arg_index]
        elem2_arg = elem2.arguments()[arg_index]
        arg_intersections.append(intersect(elem1_arg, elem2_arg, dynamic_programming_table))
    return arg_intersections

def intersect(vs1, vs2, dynamic_programming_table=None):
    if dynamic_programming_table is None: dynamic_programming_table = {}

    dynamic_programming_key = (id(vs1), id(vs2))
    if dynamic_programming_key in dynamic_programming_table:
        return dynamic_programming_table[dynamic_programming_key]
    intersection = Union([])
    if type(vs1) is Number and type(vs2) is Number:
        if vs1.n == vs2.n:
            intersection = vs1
    elif type(vs1) is ConstantString and type(vs2) is ConstantString:
        if vs1.content == vs2.content:
            intersection = vs1
    elif type(vs1) is StringVariable and type(vs2) is StringVariable:
        if vs1.name == vs2.name:
            intersection = vs1
    elif type(vs1) is Concatenate and type(vs2) is Concatenate:
        arg_intersections = intersect_args(vs1, vs2, dynamic_programming_table)
        if all( arg_intersection != Union([]) for arg_intersection in arg_intersections):
            intersection = Concatenate(*arg_intersections)
    elif type(vs1) is Substring and type(vs2) is Substring:
        arg_intersections = intersect_args(vs1, vs2, dynamic_programming_table)
        if all( arg_intersection != Union([]) for arg_intersection in arg_intersections):
            intersection = Substring(*arg_intersections)
    elif type(vs1) is Union and type(vs2) is Union:
        union_members = set()
        for member1 in vs1.members:
            for member2 in vs2.members:
                intersect_members = intersect(member1, member2, dynamic_programming_table)
                union_members.add(intersect_members)
        intersection = Union.make(union_members)
    dynamic_programming_table[dynamic_programming_key] = intersection
    return intersection          



def flashfill(input_outputs):
    """
    input_outputs: a list of input-output examples (each example is a tuple of environment and the target output)
    returns: the version space of all solutions to we synthesis problem
    
    You should call your implementation of `intersect` and also `flashfill_one_example`.
    """
    # assert False, "implement as part of homework"
    version_spaces = []
    # Run synthesizer on each example
    for input, output in input_outputs:
        version_spaces.append(flashfill_one_example(input, output))
    solution = version_spaces[0]
    for vs in version_spaces[1:]:
        solution = intersect(vs, solution)
    return solution

    
def test_flashfill():
    # collection of input-output specifications
    test_cases = []
    test_cases.append([ ({"input1": "test"}, "t") ])
    test_cases.append([ ({"input1": "121"}, "1") ])
    test_cases.append([ ({"input1": "test"}, "t"),
                        ({"input1": "121"}, "1") ])
    test_cases.append([ ({"input1": "xyz"}, "xyz") ])
    test_cases.append([ ({"input1": "xyz"}, "Dr xyz") ])
    test_cases.append([ ({"input1": "abcdefgh"}, "Dr abcdefgh") ])
    test_cases.append([ ({"input1": "xyz"}, "Dr xyz"),
                        ({"input1": "abcdefgh"}, "Dr abcdefgh")])
    test_cases.append([ ({"input1": "y"}, "abc")])
    test_cases.append([ ({"input1": "z"}, "abcdefgh")])
    test_cases.append([ ({"input1": "y"}, "abcdefgh"),
                        ({"input1": "z"}, "abcdefgh") ])
    test_cases.append([ ({"input1": "June",    "input2": "14", "input3": "1997"}, "1997, June 14")])
    test_cases.append([ ({"input1": "June",    "input2": "14", "input3": "1997"}, "1997, June 14"),
                        ({"input1": "October", "input2": "2",  "input3": "2012"}, "2012, October 2")])
    test_cases.append([ ({"input1": "555-360-9792"}, "(555) 360-9792"),
                        ({"input1": "425-923-7777"}, "(425) 923-7777") ])

    for input_outputs in test_cases:

        print()

        start_time = time.time()
        version_space = flashfill(input_outputs)
        
        print("\tran synthesizer in time", time.time() - start_time, "seconds")

        version_space_size = version_space.version_space_size()
        print("\tversion space contains",version_space_size,"programs")
        
        if version_space_size == 0:
            print("Based on the input-outputs:")
            for training_input, training_output in input_outputs:
                print("\t",training_input,f" --> '{training_output}'")
            print("You constructed an empty version space.")
            print()
            assert False, "test case failed"

        tractable = version_space_size < 10000
        
        if tractable:
            print("\tverifying everything in version space satisfies input-outputs.")
            expressions = version_space.extension()
        else:
            print("\tverifying minimum cost member of version space satisfies input-outputs.")
            expressions = [version_space.minimum_cost_member_of_extension()]
            
        for expression in expressions:
            for environment, target_output in input_outputs:
                predicted_output = expression.evaluate(environment)
                if predicted_output != target_output:
                    print("Based on the input-outputs:")
                    for training_input, training_output in input_outputs:
                        print("\t",training_input,f" --> '{training_output}'")
                    print("You constructed a version space containing the following program:")
                    print("\t",expression)
                    print("Which, when pretty printed, looks like:")
                    print("\t",expression.pretty_print())
                    print(f'This predicts the incorrect output: "{predicted_output}"')
                    print()
                    assert False, "test case failed"

        print("\t[+] passed synthesis test case:")
        for training_input, training_output in input_outputs:
            print("\t\t",training_input,f" --> '{training_output}'")
        print("\t\twith the program:")
        to_print = version_space.minimum_cost_member_of_extension().pretty_print()
        print("\t\t", to_print)
        print("\t\tequivalently:\n\t\t",
              re.sub("Substring\\(input(.), 0, -1\\)", "input\\1", to_print))
            
    print(" [+] flashfill passes checks")
    
if __name__ == "__main__":
    test_flashfill()
    
