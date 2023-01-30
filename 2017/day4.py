from itertools import permutations

valid = 0
with open("input4.txt") as file:
  for phrase in file:
    words = phrase.strip().split(" ")
    word_set = set(words)
    print(words, word_set)
    if len(words) == len(word_set):
      found_anagram = False
      for word in words:
        for anagram_set in permutations(word):
          anagram = "".join(anagram_set)
          if anagram != word and anagram in word_set:
            found_anagram = True
            
      if not found_anagram:
        valid += 1
        print("^^ valid:", valid)
      else:
        print("XX invalid anagram:", valid)
    else:
      print("XX invalid length:", valid)
      
print(valid)
  
  