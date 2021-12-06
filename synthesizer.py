# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import openai
from decouple import config
from readability import *
from inputs import inputs
from verifier import verify
from data.features import *
from data.costFuncWithFeatures import featureBasedCost

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
            engine="davinci",
            prompt=problem.get("query") + " :\n\npublic static " + problem.get("type"),
            temperature=1,
            max_tokens=100,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )

        code = response.choices[0].text
        

        passes_tests = verify(code, problem)
        
        if(passes_tests):
            correct_program_count += 1
            classification = classifier(code)
            classification_cost = cost(classification)
            feature_cost = featureBasedCost(code)
            valid_programs.append((code, classification_cost, feature_cost))
            print("CORRECT")
            print("\tCode: ", code, "\n\tScore: ", classification_cost, ", ", feature_cost)
        else:
            wrong_program_count += 1
            print("INCORRECT")
            print("\tCode: ", code)
        
        print("Correct programs generated: ", correct_program_count)
        print("Incorrect programs generated: ", wrong_program_count)
        print("===================================================================")

    valid_programs.sort(key=lambda a: a[1])

    print("Valid Synthesized Programs:")
    for program in valid_programs:
        code = program[0]
        print("\tCode: ", code)
        print("\tClassification Score: ", program[1])
        print("\Feature Score: ", program[2])
        print("\tNumber of brackets: ", numBrackets(code))
        print("\tNumber of characters:  ", len(code))
        print("\tTime complexity: ", timeComplexity(code))

    final_classification_cost = 500
    final_feature_cost = 500
    final_code = ""
    final_file = open("synthesizedProgram.java", "w")
    for code, classification_cost, feature_cost in valid_programs:
        
        final_file.write("//Program: \n")
        final_file.write(code.strip() + "\n")
        final_file.write("//Classification Cost: " + str(classification_cost) + "\n")
        final_file.write("//Feature Cost: " + str(feature_cost) + "\n")
        final_file.write("//===================================================\n")

        if (classification_cost < final_classification_cost - 5 or 
        (classification_cost > final_classification_cost - 5 and 
        classification_cost < final_classification_cost)):
            if feature_cost < final_feature_cost:
                final_classification_cost = classification_cost
                final_feature_cost = feature_cost
                final_code = code
    
    final_file.write("\n\n//Synthesized Program:\n")
    final_file.write(final_code.strip() + "\n")
    final_file.write("//Program classification cost: " + str(final_classification_cost) + "\n")
    final_file.write("//Program feature cost: " + str(final_feature_cost))
    final_file.close()

    
