# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import openai
from decouple import config
import subprocess
import os
from readability import *

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


def java_format(function, return_type):
    ret_str = ""

    # Import statements
    import_str = "import java.io.*;"
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
        parsed_arr = arg.strip().split(" ")
        if len(parsed_arr) > 2:
            arg_type = "".join(parsed_arr[:-1])
        else:
            arg_type = parsed_arr[0]

        function_args.append(arg_type)


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

            if arg_type in context.keys():
                test_args += context[arg_type]
            else:
                raise ValueError

        test_args += ")"
        main_str += "writeFile(writer, String.valueOf(" + \
            function_name + test_args + "));\n"
    main_str += "closeFile(writer);\n"
    ret_str += main_str

    ret_str += "}\n}"

    return (ret_str, expected_arr)


def clear_file():
    file = open("codeTestOutput.txt", "r+")
    file.truncate(0)
    file.close()

def verify_tests(expected_results):
    with open("codeTestOutput.txt") as file_reader:
        count = 0

        # Check if file is empty
        file_reader.seek(0, os.SEEK_END)
        if(file_reader.tell()):
            file_reader.seek(0)
        else:
            return False

        for line in file_reader:
            if line.strip() != expected_results[count]:
                return False
            count += 1
        return True


if __name__ == "__main__":
    valid_programs = []
    correct_program_count = 0
    wrong_program_count = 0
    while correct_program_count < 4:
        # Clear file as precaution
        clear_file()

        response = openai.Completion.create(
            engine="davinci",
            prompt=synthesis_function + " :\n\npublic static " + synthesis_type,
            temperature=1,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        code = response.choices[0].text
        classification = classifier(code)
        code_cost = cost(classification)

        print("\tCode: ", code, "\n\tScore: ", code_cost)

        try:
            code_file = open("codeFile.java", "w")
            formatted_java, expected_results = java_format(
                code, synthesis_type)
            code_file.write(formatted_java)
            code_file.close()

            subprocess.call("./execute_synthesized_function.sh")

            passes_tests = verify_tests(expected_results)
        except ValueError:
            passes_tests = False

        if(passes_tests):
            correct_program_count += 1
            valid_programs.append((code, code_cost))
        else:
            wrong_program_count += 1
        print("Correct programs generated: ", correct_program_count)
        print("Incorrect programs generated: ", wrong_program_count)
        print("===================================================================")

    final_cost = 500
    final_code = ""
    final_file = open("synthesizedProgram.java", "w")
    for code, cost in valid_programs:
        
        final_file.write("//Program: \n")
        final_file.write(code.strip() + "\n")
        final_file.write("//Cost: " + str(cost) + "\n")
        final_file.write("//===================================================\n")

        if cost < final_cost:
            final_cost = cost
            final_code = code
    
    final_file.write("\n\n//Synthesized Program:\n")
    final_file.write(final_code.strip() + "\n")
    final_file.write("//Program cost: " + str(final_cost))
    final_file.close()
    
