# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import os
import openai
from decouple import config
from collections import defaultdict
from transformers import GPT2TokenizerFast
import numpy as np


openai.api_key = config('OPENAI_TOKEN')

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

labels = ["Readable", "Semireadable", "Sortaunreadable", "Unreadable"]
label = [label.strip().lower().capitalize() for label in labels]

labels_tokens = {label: tokenizer.encode(" " + label) for label in labels}
print(labels_tokens)

# TEST SET
result = openai.Classification.create(
    query="def add_1(arr):\n  return map(lambda x: x + 1, arr)",
    search_model="ada", 
    model="davinci-codex",
    logprobs=5,
    labels=labels,
    examples=[
        ["def contains(item, arr):\n    return item in arr", "Readable"],
        ["def find_object(target_obj, arr):\n    for item in arr:\n        if item == target_obj:\n            return True\n\n    return False", "Semireadable"],
        ["def elem_in_list(element, check_list):\n  len_list = len(check_list)\n  for ind in range(len_list):\n    if check_list[ind] == element:\n      return True\n  \n  return False", "Sortaunreadable"],
        ["def obj_in_array(target_obj, arr):\n    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None", "Unreadable"],
        ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr", "Readable"],
        ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr", "Semireadable"],
        ["def add_one(arr):\n  return [elem + 1 for elem in arr]", "Semireadable"],
        ["def add_one(arr):\n  return map(lambda x: x + 1, arr)", "Readable"],
    ]
)

# Take the starting tokens for probability estimation.
# Labels should have distinct starting tokens.
# Here tokens are case-sensitive.
first_token_to_label = {tokens[0]: label for label, tokens in labels_tokens.items()}
# print("FTTL: ", first_token_to_label)
# print("labels tokens items: ", labels_tokens.items())

top_logprobs = result["completion"]["choices"][0]["logprobs"]["top_logprobs"][0]
print("top logprobs: ", top_logprobs)
print("Result: ", result)
token_probs = {
    tokenizer.encode(token)[0]: np.exp(logp) 
    for token, logp in top_logprobs.items()
}
label_probs = {
    first_token_to_label[token]: prob 
    for token, prob in token_probs.items()
    if token in first_token_to_label
}

print("Labels: ", label_probs)
# Fill in the probability for the special "Unknown" label.
if sum(label_probs.values()) < 1.0:
    label_probs[791] += 1.0 - sum(label_probs.values())

print(label_probs)
"""Output:
{'Negative': 0.053965452806285695,
 'Positive': 0.901394752718519,
 'Unknown': 0.04463979447519528}
"""
