import os
import subprocess

def java_format(function, problem):
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
    ret_str += "public static " + problem.get("type") + function + "\n\n"

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
    for context, expected in problem.get("test_cases"):
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

def verify(code, problem):
    try:
        code_file = open("codeFile.java", "w")
        formatted_java, expected_results = java_format(
            code, problem)
        code_file.write(formatted_java)
        code_file.close()

        subprocess.call("./execute_synthesized_function.sh")

        return verify_tests(expected_results)
    except ValueError:
        return False
