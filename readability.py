# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import os
import openai
from decouple import config
from collections import defaultdict


openai.api_key = config('OPENAI_TOKEN')

# RUN WHEN ADDING CLASSIFICATIONS TO TRAINING SET
# openai.File.create(file=open("project_training_data.jsonl"), purpose="classifications")

num_ids = len(openai.File.list().data)
print(num_ids)
id = openai.File.list().data[num_ids - 1].id
print(id)

# TEST SET
response = openai.Classification.create(
    file=id,
    query="def add_1(arr):\n  return map(lambda x: x + 1, arr)",
    search_model="ada", 
    model="davinci-codex",
    logprobs=10
)

print(response)
labels_dict = defaultdict(lambda: (0, 0))

training_examples = response.selected_examples
for example in training_examples:
    ex_label = example.label
    ex_score = example.score
    label_score, num_labels = labels_dict[ex_label]
    labels_dict[ex_label] = (label_score + ex_score, num_labels + 1)

