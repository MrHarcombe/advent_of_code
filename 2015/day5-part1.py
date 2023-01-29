string = "ugknbfddgicrmopn"
string = "aaa"
string = "jchzalrnumimnmhp"
string = "haegwjzuvuyypxyu"
string = "dvszwmarrgswjxmb"

def check_vowels(string):
  vowels = 0
  vowels += string.count("a")
  vowels += string.count("e")
  vowels += string.count("i")
  vowels += string.count("o")
  vowels += string.count("u")
  return vowels >= 3

def check_doubles(string):
  for i in range(len(string)-1):
    if string[i] == string[i+1]:
      return True
  return False

def check_barred(string):
  barred = 0
  barred += string.count("ab")
  barred += string.count("cd")
  barred += string.count("pq")
  barred += string.count("xy")
  return barred > 0

nbr_nice = 0
with open("input.txt") as f:
  string = f.readline().strip()
  while string != "":
    nice = check_vowels(string) and check_doubles(string) and not check_barred(string)
    print(string,"->",nice)
    if nice:
      nbr_nice += 1
    string = f.readline().strip()
print(nbr_nice)