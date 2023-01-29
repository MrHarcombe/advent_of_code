import re

pairs = re.compile(r'(?P<pair>..).*(?P=pair)')
between = re.compile(r'(?P<single>.).(?P=single)')

string = "qjhvhtzxzqqjkmpb"
string = "xxyxx"
string = "uurcxstgmygtbstg"
string = "ieodomkazucvgmuy"

nbr_nice = 0
with open("input.txt") as f:
  string = f.readline().strip()
  while string != "":
    match_pair = pairs.search(string)
    #if match_pair != None:
    #  print(match_pair.group("pair"))
    match_single = between.search(string)
    #if match_single != None:
    #  print(match_single.group("single"))

    nice = match_pair != None and match_single != None
    if nice:
      nbr_nice += 1
    print(string,"->",nice)
    string = f.readline().strip()
print(nbr_nice)