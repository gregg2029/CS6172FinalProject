# To activate env run: $ source activate cs6172_env
# To deactivate env run $ conda deactivate

import os
import torch
import openai
from decouple import config
# from collections import defaultdict
import numpy as np
from readability import *


openai.api_key = config('OPENAI_TOKEN')


for x in range(10):
  response = openai.Completion.create(
    engine="davinci",
    prompt="Create a python function that adds one to each element in a list :\n\ndef",
    temperature=1,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
  )

  code = response.choices[0].text
  classification = classifier(code)
  cost = cost(classification)

  print("Code: ", code, "\n\tScore: ", cost)
