# add dictionaries with the properties query, type, and test_cases to synthesize new problems
inputs = [
  {
    "query": "Create a java function that finds if an item is in an int array",
    "type": "boolean",
    "test_cases": [
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "3"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "7"}, "false"),
      ({"int[]": "new int[] {1, 2, 3, 4}", "int": "4"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "4"}, "true"),
      ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "6"}, "false")
    ]
  },
  {
    "query": "Create a java function that returns the nth value of the fibonacci sequence",
    "type": "int",
    "test_cases": [
      ({"int": "3"}, "2"),
      ({"int": "6"}, "8"),
      ({"int": "1"}, "1"),
      ({"int": "2"}, "1"),
      ({"int": "5"}, "5")
    ]
  },
  {
    "query": "Create a java function that reverses an input string",
    "type": "String",
    "test_cases": [
      ({"String": "\"hello\""}, "olleh"),
      ({"String": "\"xyx\""}, "xyx"),
      ({"String": "\"hey there\""}, "ereht yeh")
    ]
  }

]
