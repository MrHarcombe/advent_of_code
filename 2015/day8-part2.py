import json

string = '""' # 2 6
#string = '"abc"' # 5 9
#string = '"aaa\\"aaa"' # 10 16
#string = '"\\x27"' # 6 11

total_inputs = 0
total_json = 0

with open("input.txt") as f:
  string = f.readline().strip()

  while string != "":
    print(len(string), len(json.dumps(string)))

    total_inputs += len(string)
    total_json += len(json.dumps(string))

    string = f.readline().strip()

print(total_inputs, total_json, total_json - total_inputs)
