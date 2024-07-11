import csv
import time

from openai import OpenAI

PRIMARY_DIRECTORY = 'C:\\Users\\brend\\OneDrive\\Desktop\\School\\REX Computational Science 2024\\Japanese Translation\\Data\\'


# PARAMETER = 0.9
PARAMETER = ""

# Function Definitions
def gptTranslation(input, temp, topp):
  return client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": "translate " + input + " into English without explanation"}
    ],
    user="gptTranslator_py",
    top_p=topp,
    temperature=temp
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
gpt_key = 'sorry, I am not giving this to you'
client = OpenAI(
  api_key=gpt_key,
)

# Translation Request Guidelines
BURST_DELAY = 70.0
BURST_REQUESTS = 499


def translateCorpus(japaneseSentences, TEMPERATURE, TOPP):
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
      response = gptTranslation(sentence, TEMPERATURE, TOPP)
      input_tokens_used += response.usage.prompt_tokens
      output_tokens_used += response.usage.completion_tokens
      translations.append([outputCleanup(response.choices[0].message.content)])
      successfulRequests += 1
    except Exception as e:
      print(e)
      translations.append(["**FAILURE** (" + str(e) + ") : "+ sentence])

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
  filename = 'gptData' + str(TEMPERATURE).replace('.', '') + "-" + str(TOPP).replace('.', '') + '.csv'
  with open(PRIMARY_DIRECTORY + filename, 'w', newline='', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerows(translations)
    print("Write Successful: " + PRIMARY_DIRECTORY + filename)

for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0][::-1]:
  for p in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0][::-1]:
    translateCorpus(japaneseSentences, t, p)