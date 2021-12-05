import openai

def numBrackets(code):
  count = 0
  for character in code:
    if character == "{":
      count = count + 1
  return count

def timeComplexity(code):
  response = openai.Completion.create(
    engine="davinci-codex",
    prompt=code + "\n### The time complexity of this function is",
    stop=['###', '\n'],
  )
  return response["choices"][0]["text"]
