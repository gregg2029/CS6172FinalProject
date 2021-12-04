from decouple import config
import openai
from trainingSet import onlyFunctions

openai.api_key = config('OPENAI_TOKEN')

response = openai.Engine("davinci-codex").search(
  documents=onlyFunctions,
  query="the most readable function"
)

print(response)
