import openai

def numChar(code, char):
  count = 0
  for character in code:
    if character == char:
      count = count + 1
  return count

def numBrackets(code):
  return numChar(code, "{")

def numParen(code):
  return numChar(code, "(")

def numSemicolan(code):
  return numChar(code, ";")

def lengthOfCode(code):
  return numBrackets(code) + numParen(code) + numSemicolan(code)

def timeComplexity(code):
  response = openai.Completion.create(
    engine="davinci-codex",
    prompt=code + "\n### The time complexity of this function is",
    stop=['###', '\n'],
  )
  return response["choices"][0]["text"]
