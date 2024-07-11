import csv
import time

from transformers import BertTokenizer, BertForMaskedLM, BertModel
from bert_score import BERTScorer

PRIMARY_DIRECTORY = 'C:\\Users\\brend\\OneDrive\\Desktop\\School\\REX Computational Science 2024\\Japanese Translation\\Data\\'

# Function Definitions
def bertEval(ref, cand):
  P, R, F1 = bert.score([cand], [ref])
  return [F1, P, R]

# Read Translation Files
refSentences = []
with open(PRIMARY_DIRECTORY + 'eData.csv', newline='', encoding="utf8") as csvFile:
  dialect = csv.Sniffer().sniff(csvFile.read(1024))
  csvFile.seek(0)
  reader = csv.reader(csvFile, dialect)
  for row in reader:
    refSentences.append(row[0])

print("Read Successful: " + PRIMARY_DIRECTORY + 'eData.csv')
print(len(refSentences))
print("")

# Create BERT Scorer Object
bert = BERTScorer(model_type='bert-base-uncased')
time.sleep(2)

def doBERT(temperature, topp):
  geminiSentences = []
  with open(PRIMARY_DIRECTORY + 'geminiData' + temperature + '-' + topp + '.csv', newline='', encoding="utf8") as csvFile:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for row in reader:
      geminiSentences.append(row[0])

  print("Read Successful: " + PRIMARY_DIRECTORY + 'geminiData' + temperature + '-' + topp + '.csv')
  print(len(geminiSentences))
  print("")

  gptSentences = []
  with open(PRIMARY_DIRECTORY + 'gptData' + temperature + '-' + topp + '.csv', newline='', encoding="utf8") as csvFile:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for row in reader:
      gptSentences.append(row[0])

  print("Read Successful: " + PRIMARY_DIRECTORY + 'gptData' + temperature + '-' + topp + '.csv')
  print(len(gptSentences))
  print("")

  googleSentences = []
  with open(PRIMARY_DIRECTORY + 'googleData.csv', newline='', encoding="utf8") as csvFile:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for row in reader:
      googleSentences.append(row[0])

  print("Read Successful: " + PRIMARY_DIRECTORY + 'googleData.csv')
  print(len(googleSentences))
  print("")

  mSentences = []
  with open(PRIMARY_DIRECTORY + 'mData.csv', newline='', encoding="utf8") as csvFile:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for row in reader:
      mSentences.append(row[0])

  print("Read Successful: " + PRIMARY_DIRECTORY + 'mData.csv')
  print(len(mSentences))
  print("")

  # Evaluation
  fScores = ["BERT-F1", 0, 0, 0, 0]
  precisions = ["BERT-P", 0, 0, 0, 0]
  recalls = ["BERT-R", 0, 0, 0, 0]

  successfulRequests = 0
  totalRequests = 0

  for i in range(0, len(refSentences), 1):
    try:
      geminiBertScore = bertEval(refSentences[i], geminiSentences[i])
      gptBertScore = bertEval(refSentences[i], gptSentences[i])
      googleBertScore = bertEval(refSentences[i], googleSentences[i])
      mBertScore = bertEval(refSentences[i], mSentences[i])

      fScores[1] += float(geminiBertScore[0].mean())
      fScores[2] += float(gptBertScore[0].mean())
      fScores[3] += float(googleBertScore[0].mean())
      fScores[4] += float(mBertScore[0].mean())

      precisions[1] += float(geminiBertScore[1].mean())
      precisions[2] += float(gptBertScore[1].mean())
      precisions[3] += float(googleBertScore[1].mean())
      precisions[4] += float(mBertScore[1].mean())

      recalls[1] += float(geminiBertScore[2].mean())
      recalls[2] += float(gptBertScore[2].mean())
      recalls[3] += float(googleBertScore[2].mean())
      recalls[4] += float(mBertScore[2].mean())

      successfulRequests += 1
    except ValueError as ve:
      print(ve)
    
    totalRequests += 1
    print(totalRequests)
    print([fScores, precisions, recalls])

  print("-----------------------------------")
  print(fScores)
  print(precisions)
  print(recalls)
  print("")

  for i in range(1, 5):
    fScores[i] /= totalRequests
    precisions[i] /= totalRequests
    recalls[i] /= totalRequests

  print("Successful Requests: " + str(successfulRequests) + " / " + str(totalRequests))
  print(fScores)
  print(precisions)
  print(recalls)
  print("")

  # Append to resultsData.csv
  resultsData = []
  with open(PRIMARY_DIRECTORY + 'resultsData' + temperature + '-' + topp + '.csv', newline='', encoding="utf8") as csvFile:
    dialect = csv.Sniffer().sniff(csvFile.read(1024))
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for row in reader:
      resultsData.append(row)
  print("Read Successful: " + PRIMARY_DIRECTORY + 'resultsData' + temperature + '-' + topp + '.csv')
  print(len(resultsData))
  print("")

  resultsData.append(fScores)
  resultsData.append(precisions)
  resultsData.append(recalls)

  with open(PRIMARY_DIRECTORY + 'resultsData' + temperature + '-' + topp + '.csv', 'w', newline='', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerows(resultsData)
    print("Write Successful: " + PRIMARY_DIRECTORY + 'resultsData' + temperature + '-' + topp + '.csv')

  # Output State: {"Metric", "Gemini-1.5 Flash", "GPT-3.5 Turbo", "Google Tranlsate", "Microsoft Translate"}

for t in range(14, 21, 2):
  # for tp in range(0, 11, 1):
    if len(str(t)) < 2:
      t = "0" + str(t)
    # if len(str(tp)) < 2:
    #   tp = "0" + str(tp)
    
    doBERT(str(t), str(10))
