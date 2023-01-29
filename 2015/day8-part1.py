string = '""' # 2 0
string = '"abc"' # 5 3
string = '"aaa\\"aaa"' # 10 7
string = '"\\x27"' # 6 1

total_inputs = 0
total_eval = 0

with open("input.txt") as f:
  string = f.readline().strip()

  while string != "":
    print(len(string))
    print(len(eval(string)))

    total_inputs += len(string)
    total_eval += len(eval(string))

    string = f.readline().strip()

print(total_inputs, total_eval, total_inputs - total_eval)