# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import openai
from decouple import config
from readability import *
from inputs import inputs
from verifier import verify
from data.features import *

openai.api_key = config('OPENAI_TOKEN')

# details of the problem we want to synthesize
problem = inputs[1]

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
            engine="davinci-codex",
            prompt=problem.get("query") + " :\n\npublic static " + problem.get("type"),
            temperature=0,
            max_tokens=680,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        code = response.choices[0].text
        

        passes_tests = verify(code, problem)
        
        if(passes_tests):
            correct_program_count += 1
            classification = classifier(code)
            code_cost = cost(classification)
            valid_programs.append((code, code_cost))
            print("CORRECT")
            print("\tCode: ", code, "\n\tScore: ", code_cost)
        else:
            wrong_program_count += 1
            print("INCORRECT")
            print("\tCode: ", code)
        
        print("Correct programs generated: ", correct_program_count)
        print("Incorrect programs generated: ", wrong_program_count)
        print("===================================================================")

    valid_programs = [
        ('fib ( int n ) { if ( n < 2 ) return n ; else return fib ( n - 1 ) + fib ( n - 2 ); }', 18.017825940242005),
        ('valueN(int n ) { return n <= 2 ? 1 : valueN(n - 1) + valueN(n - 2); }', 22.940791652726006),
        ('fibonacci ( int i ) { if ( i == 0 ) { return 0 ; } else if ( i == 1 ) { return 1 ; } else { return fibonacci ( i - 1 ) + fibonacci ( i - 2 ); } }', 24.092495652995513),
        ('getFibValue(int i) { if (i <= 1) { return i; } else { return getFibValue(i-2) + getFibValue(i-1); } }', 24.460495742297205)
    ]
    valid_programs.sort(key=lambda a: a[1])

    print("Valid Synthesized Programs:")
    for program in valid_programs:
        code = program[0]
        print("\tCode: ", code)
        print("\tScore: ", program[1])
        print("\tNumber of brackets: ", numBrackets(code))
        print("\tNumber of characters:  ", len(code))
        print("\tTime complexity: ", timeComplexity(code))

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

    
