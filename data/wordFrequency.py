from collections import defaultdict

tokenFreq = defaultdict(lambda: 0)

with open("Tokens.txt", "r") as input:
  for line in input: 
    for word in line.split():
      #print(word, "\n")
      tokenFreq[word.lower()] += 1
tokenFreq = sorted(tokenFreq.items(),key= lambda item: item[1], reverse = True)

#print(tokenFreq)

with open("MostFrequentTokens.txt", "a") as output: 
    for item in tokenFreq:
        outputL = item[0] + ", " + str(item[1])
        output.write(outputL)
        output.write("\n")