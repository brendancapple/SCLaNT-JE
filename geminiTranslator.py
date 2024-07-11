import csv
import time

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

PRIMARY_DIRECTORY = 'C:\\Users\\brend\\OneDrive\\Desktop\\School\\REX Computational Science 2024\\Japanese Translation\\Data\\'

# PARAMETER = 0.9
PARAMETER = ""

# Function Definitions
def geminiTranslation(input):
  return gemini.generate_content("translate " + input + " into English without explanation", 
      safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }, generation_config=genai.types.GenerationConfig(
        # top_p=PARAMETER
        )
  )

def outputCleanup(input):
  output = input.strip()
  # if ',' not in output:
  #  output = "\"" + output + "\""

  return output

# Read jData.csv File
japaneseSentences = []
with open(PRIMARY_DIRECTORY + 'jData.csv', newline='', encoding="utf8") as csvFile:
  dialect = csv.Sniffer().sniff(csvFile.read(1024))
  csvFile.seek(0)
  reader = csv.reader(csvFile, dialect)
  for row in reader:
    japaneseSentences.append(row[0])

print("Read Successful: " + PRIMARY_DIRECTORY + 'jData.csv')
print("")
print(japaneseSentences)
print("")
time.sleep(2)

# Connect to the Gemini API
gemini_key = 'sorry, I am not giving this to you'
genai.configure(api_key=gemini_key)
gemini = genai.GenerativeModel('gemini-1.5-flash')

# Translation Request Guidelines
BURST_DELAY = 70.0
BURST_REQUESTS = 499

# Make Translation Requests
translations = []

requestCount = 0
successfulRequests = 0
totalRequests = 0
input_tokens_used = 0
output_tokens_used = 0
updateTime = time.time()
startTime = updateTime

print("Start: " + str(startTime))

for sentence in japaneseSentences:
  try:
    response = geminiTranslation(sentence)
    input_tokens_used += response.usage_metadata.prompt_token_count
    output_tokens_used += response.usage_metadata.candidates_token_count
    translations.append([outputCleanup(response.text)])
    successfulRequests += 1
  except ValueError as ve:
    print(ve)
    print(response.candidates)
    translations.append(["**FAILURE** (" + str(ve) + ") : "+ sentence])

  totalRequests += 1
  requestCount += 1
  print(totalRequests)
  print(translations[-1])

  if requestCount >= BURST_REQUESTS:
    print("Time Elapsed: " + str(int(time.time() - startTime)))
    timeRemaining = (updateTime + BURST_DELAY) - time.time()
    print(str(int(timeRemaining)) + " / " + str(int(BURST_DELAY)))
    print("Requests this Minute: " + str(requestCount) + " / " + str(BURST_REQUESTS))
    print("Requests: " + str(totalRequests) + " / " + str(len(japaneseSentences)))
    print("Successful Requests: " + str(successfulRequests) + " / " + str(totalRequests))
    print("Input Tokens: " + str(input_tokens_used))
    print("Response Tokens: " + str(output_tokens_used))
    print("")

    while time.time() - updateTime < BURST_DELAY:
      time.sleep(0.5)

    updateTime = time.time()
    requestCount = 0

print("Successful Requests: " + str(successfulRequests) + " / " + str(totalRequests))
print("Input Tokens: " + str(input_tokens_used))
print("Response Tokens: " + str(output_tokens_used))
print("")
# print(translations)

# Write to geminiRawData.csv
filename = 'geminiData' + str(PARAMETER).replace('.', '') + '.csv'

with open(PRIMARY_DIRECTORY + filename, 'w', newline='', encoding="utf8") as f:
  writer = csv.writer(f)
  writer.writerows(translations)
  print("Write Successful: " + PRIMARY_DIRECTORY + filename)