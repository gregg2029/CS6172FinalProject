tab = "\t"

class Expression():

    def evaluate(self, environment):
        assert False, "not implemented"

    # list of expressions
    def arguments(self):
        assert False, "not implemented"

    def cost(self):
        return 1 + sum([0] + [argument.cost() for argument in self.arguments()])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self): return hash(str(self))

    def __ne__(self, other): return str(self) != str(other)

    def __gt__(self, other): return str(self) > str(other)

    def __lt__(self, other): return str(self) < str(other)

    def minimum_cost_member_of_extension(self):
        assert False, "implement as part of homework"

    def version_space_size(self):
        assert False, "implement as part of homework"


class FALSE(Expression):
    return_type = "bool"
    argument_types = []

    def __init__(self): pass

    def __str__(self):
        return "False"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += "False"
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        return False

    def arguments(self):
        return []

    def cost(self):
        return 1


class Number(Expression):
    return_type = "int"
    argument_types = []

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return f"Number({self.n})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += str(self.n)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        return self.n

    def arguments(self):
        return []

    def cost(self):
        if self.n == 0 or self.n == -1:
            return 1
        else:
            return 10
    
    def version_space_size(self):
        return 1
    
    def extension(self):
        return [self]
    
    def minimum_cost_member_of_extension(self):
        return self


class NumberVariable(Expression):
    return_type = "int"
    argument_types = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"NumberVariable('{self.name}')"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += self.name
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        return environment[self.name]

    def arguments(self):
        return []

    def cost(self):
        return 1
    
    def version_space_size(self):
        return 1


class Plus(Expression):
    return_type = "int"
    argument_types = ["int", "int"]

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Plus({self.x}, {self.y})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += self.x.pretty_print(indent, False, False) + " + " + self.y.pretty_print(indent, False, False)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        x = self.x.evaluate(environment)
        y = self.y.evaluate(environment)
        assert isinstance(x, int) and isinstance(y, int)
        return x + y

    def arguments(self):
        return [self.x, self.y]


class Times(Expression):
    return_type = "int"
    argument_types = ["int", "int"]

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Times({self.x}, {self.y})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += self.x.pretty_print(indent, False, False) + " * " + self.y.pretty_print(indent, False, False)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        x = self.x.evaluate(environment)
        y = self.y.evaluate(environment)
        assert isinstance(x, int) and isinstance(y, int)
        return x * y

    def arguments(self):
        return [self.x, self.y]


class LessThan(Expression):
    return_type = "bool"
    argument_types = ["int", "int"]

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"LessThan({self.x}, {self.y})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += self.x.pretty_print(indent, False, False) + " < " + self.y.pretty_print(indent, False, False)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        x = self.x.evaluate(environment)
        y = self.y.evaluate(environment)
        assert isinstance(x, int) and isinstance(y, int)
        return x < y

    def arguments(self):
        return [self.x, self.y]


class And(Expression):
    return_type = "bool"
    argument_types = ["bool", "bool"]

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"And({self.x}, {self.y})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += self.x.pretty_print(indent, True, False) + " and " + self.y.pretty_print(indent, False, False)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        x = self.x.evaluate(environment)
        y = self.y.evaluate(environment)
        assert isinstance(x, bool) and isinstance(y, bool)
        return x and y

    def arguments(self):
        return [self.x, self.y]


class Not(Expression):
    return_type = "bool"
    argument_types = ["bool"]

    def __init__(self, x):
        self.x = x

    def __str__(self):
        return f"Not({self.x})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += "not " + self.x.pretty_print(indent, False, False)
        if bool_nln:
            ret_string += "\n"
        return ret_string

    def evaluate(self, environment):
        x = self.x.evaluate(environment)
        assert isinstance(x, bool)
        return not x

    def arguments(self):
        return [self.x]


class If(Expression):
    return_type = "int"
    argument_types = ["bool", "int", "int"]

    def __init__(self, test, yes, no):
        self.test, self.yes, self.no = test, yes, no

    def __str__(self):
        return f"If({self.test}, {self.yes}, {self.no})"

    def pretty_print(self, indent, bool_ind, bool_nln):
        ret_string = ""
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += "if (" + self.test.pretty_print(indent, False, False) + "):" + "\n"
        ret_string += self.yes.pretty_print(indent + 1, True, True)
        if bool_ind:
            for x in range(indent):
                ret_string += tab
        ret_string += "else:\n"
        ret_string += self.no.pretty_print(indent + 1, True, True)
        return ret_string

    def evaluate(self, environment):
        test = self.test.evaluate(environment)
        yes = self.yes.evaluate(environment)
        no = self.no.evaluate(environment)
        assert isinstance(test, bool) and isinstance(
            yes, int) and isinstance(no, int)
        return (
            yes
            if test else
            no
        )

    def arguments(self):
        return [self.test, self.yes, self.no]


def test_evaluation():
    expressions, ground_truth = [], []

    expressions.append(If(LessThan(NumberVariable("x"), NumberVariable("y")),
                          NumberVariable("x"),
                          NumberVariable("y")))
    ground_truth.append(lambda x, y: min(x, y))

    expressions.append(If(Not(LessThan(NumberVariable("x"), NumberVariable("y"))),
                          Times(NumberVariable("x"), NumberVariable("y")),
                          Plus(NumberVariable("x"), NumberVariable("y"))))
    ground_truth.append(lambda x, y: x * y if not (x < y) else x + y)

    expressions.append(Times(NumberVariable(
        "x"), Plus(NumberVariable("y"), Number(5))))
    ground_truth.append(lambda x, y: x * (y + 5))

    expressions.append(FALSE())
    ground_truth.append(lambda x, y: False)

    expressions.append(Not(FALSE()))
    ground_truth.append(lambda x, y: True)

    all_correct = True
    for expression, correct_semantics in zip(expressions, ground_truth):
        this_correct = True
        for x in range(10):
            for y in range(10):
                if expression.evaluate({"x": x, "y": y}) != correct_semantics(x, y):
                    this_correct = False
        if not this_correct:
            print("problem with evaluation for expression:")
            print(expression)
            print("please debug `evaluate` methods")
        all_correct = all_correct and this_correct

    if all_correct:
        print(" [+] arithmetic evaluation passes checks")


if __name__ == "__main__":
    test_evaluation()
