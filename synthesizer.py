# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import openai
from decouple import config
import numpy as np
import subprocess

openai.api_key = config('OPENAI_TOKEN')

# Define test set as strings
test_set = []
test_set.append(({"int[]": "new int[] {1, 2, 3, 4}", "int": "3"}, "true"))
test_set.append(({"int[]": "new int[] {1, 2, 3, 4}", "int": "7"}, "false"))
test_set.append(({"int[]": "new int[] {1, 2, 3, 4}", "int": "4"}, "true"))
test_set.append(
    ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "4"}, "true"))
test_set.append(
    ({"int[]": "new int[] {1, 2, 3, 4, 4, 4}", "int": "6"}, "false"))

# Define function to be synthesized
synthesis_function = "Create a python function that finds if an item is in an int array"

# Define function Java return type
synthesis_type = "boolean"


def classifier(query):
    labels = ["Readable", "Acceptable", "Difficult", "Unreadable"]
    labels = [label.strip().lower().capitalize() for label in labels]
    result = openai.Classification.create(
        query=query,
        search_model="ada",
        model="davinci-codex",
        logprobs=5,
        labels=labels,
        max_examples=2,
        examples=[
            ["def contains(item, arr):\n    return item in arr", "Readable"],
            ["def find_object(target_obj, arr):\n    for item in arr:\n        if item == target_obj:\n            return True\n\n    return False", "Acceptable"],
            ["def elem_in_list(element, check_list):\n  len_list = len(check_list)\n  for ind in range(len_list):\n    if check_list[ind] == element:\n      return True\n  \n  return False", "Difficult"],
            ["def obj_in_array(target_obj, arr):\n    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None", "Unreadable"],
            ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr", "Readable"],
            ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr", "Acceptable"],
            ["def add_one(arr):\n  return [elem + 1 for elem in arr]",
             "Acceptable"],
            ["def add_one(arr):\n  return map(lambda x: x + 1, arr)",
             "Difficult"],
        ]
    )

    return result


def cost(classification):
    labels = ["Readable", "Acceptable", "Difficult", "Unreadable"]
    labels = [label.strip().lower().capitalize() for label in labels]

    # Take the starting tokens for probability estimation.
    # Labels should have distinct starting tokens.
    # Here tokens are case-sensitive.
    labels = [" " + label for label in labels]
    top_logprobs = classification["completion"]["choices"][0]["logprobs"]["top_logprobs"][1]

    probs = {
        sublabel: np.exp(logp)
        for sublabel, logp in top_logprobs.items()
    }
    label_probs = {}
    for sublabel, prob in probs.items():
        for label in labels:
            if sublabel in label:
                label_probs[label] = prob

    # Fill in the probability for the special "Unknown" label.
    if sum(label_probs.values()) < 1.0:
        label_probs[" Unknown"] = 1.0 - sum(label_probs.values())

    for label_prob in label_probs.keys():
        print(label_prob, ": ", label_probs[label_prob])

    label_weights = {}
    label_weights[" Readable"] = 0.1
    label_weights[" Acceptable"] = 1
    label_weights[" Difficult"] = 10
    label_weights[" Unreadable"] = 100
    label_weights[" Unknown"] = 25

    cost = 0
    for label in label_probs.keys():
        cost += label_probs[label] * label_weights[label]

    return cost


def java_format(function, return_type):
    ret_str = ""

    # Import statements
    import_str = """import java.io.File;  // Import the File class
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
        """
    ret_str += import_str + "\n\n"

    # Create class
    ret_str += "class A{\n\n"

    # File writing functions
    file_write_str = """public static FileWriter createFile() {
  try {
    FileWriter myWriter = new FileWriter("codeTestOutput.txt");
    return myWriter;
  } 
  catch (IOException e) {
    System.out.println("An error occurred.");
    e.printStackTrace();
  }
  return null;
}

public static void writeFile(FileWriter writer, String text){
  try{
    writer.write(text + "\\n");
    return;
  } catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
  }
  return;
}

public static void closeFile(FileWriter writer){
  try{
    writer.close();
    return;
  } catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
  }
  return;
}
    """
    ret_str += file_write_str + "\n"

    # Synthesized function
    ret_str += "public static " + return_type + function + "\n\n"

    # Parse synthesized function
    function_parts = function.split("(")
    function_name = function_parts[0].strip()
    function_args_whole = function_parts[1].split(")")[0].split(",")
    function_args = []

    for arg in function_args_whole:
        arg_type = arg.strip().split(" ")[0]
        function_args.append(arg_type)

    # print("func name: ", function_name)
    # print("func args: ", function_args_whole)
    # print("arg types: ", function_args)

    # Main function
    main_str = "public static void main(String[] args){\n"
    main_str += "FileWriter writer = createFile();\n"

    expected_arr = []
    for context, expected in test_set:
        expected_arr.append(expected)
        test_args = "("
        first = True
        for arg_type in function_args:
            if not first:
                test_args += ", "
            else:
                first = False
            test_args += context[arg_type]
        test_args += ")"
        main_str += "writeFile(writer, String.valueOf(" + \
            function_name + test_args + "));\n"
    main_str += "closeFile(writer);\n"
    ret_str += main_str

    ret_str += "}\n}"

    return (ret_str, expected_arr)

def verify_tests(expected_results):
    with open("codeTestOutput.txt") as file_reader:
        count = 0
        for line in file_reader:
            if line.strip() != expected_results[count]:
                return False
            count += 1
    return True

if __name__ == "__main__":
    for x in range(1):
        response = openai.Completion.create(
            engine="davinci",
            prompt=synthesis_function + " :\n\npublic static " + synthesis_type,
            temperature=0.4,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        code = response.choices[0].text
        classification = classifier(code)
        code_cost = cost(classification)

        code_file = open("codeFile.java", "w")
        formatted_java, expected_results = java_format(code, synthesis_type)
        code_file.write(formatted_java)
        code_file.close()

        subprocess.call("./execute_synthesized_function.sh")

        passes_tests = verify_tests(expected_results)

        print("\tCode: ", code, "\n\tScore: ", code_cost)
        print("Passed: ", passes_tests)
        print("===================================================================")
