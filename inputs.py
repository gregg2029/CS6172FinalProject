# add dictionaries with the properties query, type, and test_cases to synthesize new problems
inputs = [
  {
    "query": "Create a python function that finds if an item is in an int array",
    "type": "boolean",
    "test_cases": [
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "3"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "7"}, "false"),
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "4"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "4"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "6"}, "false")
    ]
  }

]
