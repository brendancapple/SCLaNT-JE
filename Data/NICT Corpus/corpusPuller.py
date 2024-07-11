import csv

PRIMARY_DIRECTORY = 'C:\\Users\\brend\\OneDrive\\Desktop\\School\\REX Computational Science 2024\\Japanese Translation\\Data\\'
MIN_JAPANESE_CHARACTERS = 8
MIN_ENGLISH_WORDS = 6
MAX_LINES = 100

TOPICS = ["SCL", "BDS", "BLD", "CLT", "EPR", "FML", "GNM", "HST", "LTT", "PNM", "RLW", "ROD", "SAT", "SNT", "TTL"]
START_FILES = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
END_FILES = [46, 1061, 496, 2044, 772, 232, 343, 1966, 678, 4678, 290, 191, 534, 413, 367]

HIRAGANA = {'あ', 'い', 'う', 'え', 'お', 
            'か', 'き', 'く', 'け', 'こ', 
            'さ', 'し', 'す', 'せ', 'そ', 
            'た', 'ち', 'つ', 'て', 
            'な', 'に', 'ぬ', 'ね', 
            'は', 'ひ', 'ふ', 'へ', 'ほ', 
            'ま', 'み', 'む', 'め', 'も',
            'ゆ',                   'よ', 
            'ら', 'り', 'る', 'れ', 'ろ', 
            'わ',       'を',       'ん', 
            'が', 'ぎ', 'ぐ', 'げ', 'ご', 
            'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 
            'だ', 'ぢ', 'づ', 'で', 'ど', 
            'ば', 'び', 'ぶ', 'べ', 'ぼ', 
            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'}

maxLinesTopic = MAX_LINES // len(TOPICS) + 1

jCorpus = []
eCorpus = []

filesUsed = []
fileCharacters = []

jCorpusChar = 0
jCorpusWords = 0

eCorpusChar = 0
eCorpusWords = 0

def clean(str):
    output = str
    output = output.replace("&quot;", '\"')
    output = output.replace("&amp;", '&')
    output = output.replace("&apos;", '\'')
    output = output.replace("&gt;", '>')
    output = output.replace("&lt;", '<')

    return output

for t in range(0, len(TOPICS)):
    topicLines = 0
    for i in range(START_FILES[t], END_FILES[t]+1):
        file_name = TOPICS[t] + "00000"[:-len(str(i))] + str(i) + ".xml"
        path = PRIMARY_DIRECTORY  + "NICT Corpus\\BilingualCorpus-master\\BilingualCorpus-master\\wiki_corpus_2.01\\" + TOPICS[t] + "\\" + file_name
        corpusFile = open(path, "r", encoding="utf8")
        corpusArray = corpusFile.read().split('\n')
        # print(corpusArray)
        # print()

        filesUsed.append(TOPICS[t] + " " + str(i))
        fileCharacters.append(0)

        skipL = False
        for line in corpusArray:
            if '<j>' in line:
                temp = line[3:-4]
                if len(temp) < MIN_JAPANESE_CHARACTERS:
                    skipL = True
                    continue
                
                containsHiragana = False
                for char in line:
                    if char in HIRAGANA:
                        containsHiragana = True
                        break

                if not containsHiragana:
                    skipL = True
                    continue

                jCorpus.append([temp])
                jCorpusChar += len(temp)
                fileCharacters[-1] += len(temp)
                jCorpusWords += len(temp.split(' '))

            elif '<e type="check" ver="1">' in line:
                if skipL == True:
                    skipL = False
                    continue

                temp = clean(line[24:-4])
                lineWords = len(temp.split(' '))

                onlyEnglish = True
                for char in temp:
                    if ord(char) > 500:
                        onlyEnglish = False
                        break

                if (not onlyEnglish) or lineWords < MIN_ENGLISH_WORDS:
                    relevantJapanese = jCorpus[-1][0]
                    jCorpus.remove([relevantJapanese])
                    jCorpusChar -= len(relevantJapanese)
                    fileCharacters[-1] -= len(relevantJapanese)
                    jCorpusWords -= len(relevantJapanese.split(' '))
                    continue

                eCorpus.append([temp])
                eCorpusChar += len(temp)
                eCorpusWords += len(temp.split(' '))
                topicLines += 1

            if topicLines >= maxLinesTopic:
                break

        # print(jCorpus)
        print(len(jCorpus))
        # print(eCorpus)
        print(len(eCorpus))
        print()

        if topicLines >= maxLinesTopic:
            break

    print("-------------------------------")
    print("Files:  " + str(filesUsed))
    print("Char: " + str(fileCharacters))
    print()
    print("jCorpus Lines: " + str(len(jCorpus)))
    print("jCorpus Words: " + str(jCorpusWords))
    print("jCorpus Char: " + str(jCorpusChar))
    print()
    print("eCorpus Lines: " + str(len(eCorpus)))
    print("eCorpus Words: " + str(eCorpusWords))
    print("eCorpus Char: " + str(eCorpusChar))
    print()


# Write to jCorpus.csv
with open(PRIMARY_DIRECTORY + 'NICT Corpus\\jCorpus.csv', 'w', newline='', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerows(jCorpus)
    print("Write Successful: " + PRIMARY_DIRECTORY + 'NICT Corpus\\jCorpus.csv')

# Write to eCorpus.csv
with open(PRIMARY_DIRECTORY + 'NICT Corpus\\eCorpus.csv', 'w', newline='', encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerows(eCorpus)
    print("Write Successful: " + PRIMARY_DIRECTORY + 'NICT Corpus\\eCorpus.csv')

## Final Settings Used (RQ1)
#   Max Lines: 1,000 (Margin of Error 15)
#   Min Japanese Characters: 8
#   Min English Words: 6
#   Exclude lines with only names (Can tell because no hiragana characters--と and や not included, because on their own, they mean 'and')
#   Exclude lines with non-ASCII characters in the translation

# SCL 1 : 1236 Word 39793 Char
# SCL 2 : 1280 Word 37948 Char
# SCL 3 : 1213 Word 38168 Char
# SCL 4 : 1210 Word 38345 Char
# SCL 5 : 1211 Word 38392 Char
# SCL 10 : 1164 Word 39361 Char
# SCL 15 : 1141 Word 39043 Char
# SCL 20 : 1464 Word 46003 Char <-- **Best Bang per Buck**
# SCL 25 : 1467 Word 43373 Char
# SCL 30 : 1132 Word 36667 Char
# SCL 36 : 6682 Char <-- **Best File**

# ALL    : 1228 Word 51391 Char
# ALL M5 : 1233 Word 52298 Char
# ALL M6 : 1237 Word 52579 Char
# ALL と : 1234 Word 52623 Char
# ALL や : 1234 Word 52623 Char
