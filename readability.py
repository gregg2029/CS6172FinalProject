# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import os
import torch
import openai
from decouple import config
from collections import defaultdict
import numpy as np


openai.api_key = config('OPENAI_TOKEN')

real_labels = ["Readable", "Semireadable", "Sortaunreadable", "Unreadable"]
labels = ["Readable", "Acceptable", "Difficult", "Unreadable"]
labels = [label.strip().lower().capitalize() for label in labels]

# TEST SET
result = openai.Classification.create(
    query="def add_1(arr):\n  return map(lambda x: x + 1, arr)",
    search_model="ada", 
    model="davinci-codex",
    logprobs=5,
    labels=labels,
    examples=[
        ["def contains(item, arr):\n    return item in arr", "Readable"],
        ["def find_object(target_obj, arr):\n    for item in arr:\n        if item == target_obj:\n            return True\n\n    return False", "Acceptable"],
        ["def elem_in_list(element, check_list):\n  len_list = len(check_list)\n  for ind in range(len_list):\n    if check_list[ind] == element:\n      return True\n  \n  return False", "Difficult"],
        ["def obj_in_array(target_obj, arr):\n    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None", "Unreadable"],
        ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr", "Readable"],
        ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr", "Acceptable"],
        ["def add_one(arr):\n  return [elem + 1 for elem in arr]", "Acceptable"],
        ["def add_one(arr):\n  return map(lambda x: x + 1, arr)", "Readable"],
    ]
)

# Take the starting tokens for probability estimation.
# Labels should have distinct starting tokens.
# Here tokens are case-sensitive.
labels = [" " + label for label in labels]
top_logprobs = result["completion"]["choices"][0]["logprobs"]["top_logprobs"][1]
print("top_logprobs: ", top_logprobs)

probs = {
    sublabel: np.exp(logp) 
    for sublabel, logp in top_logprobs.items()
}
label_probs = {}
for sublabel, prob in probs.items():
    for label in labels:
        if sublabel in label:
            label_probs[label] = prob


print("Labels: ", label_probs)
# Fill in the probability for the special "Unknown" label.
if sum(label_probs.values()) < 1.0:
    label_probs[" Unreadable"] += 1.0 - sum(label_probs.values())

print(label_probs)
