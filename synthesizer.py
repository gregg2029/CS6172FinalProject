# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import openai
from decouple import config
from readability import *
from inputs import inputs
from verifier import verify

openai.api_key = config('OPENAI_TOKEN')

# details of the problem we want to synthesize
problem = inputs[0]

def clear_file():
    file = open("codeTestOutput.txt", "r+")
    file.truncate(0)
    file.close()

if __name__ == "__main__":
    valid_programs = []
    correct_program_count = 0
    wrong_program_count = 0
    while correct_program_count < 4:
        # Clear file as precaution
        clear_file()

        response = openai.Completion.create(
            engine="davinci",
            prompt=problem.get("query") + " :\n\npublic static " + problem.get("type"),
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
        
        passes_tests = verify(code, problem)
        
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
    
