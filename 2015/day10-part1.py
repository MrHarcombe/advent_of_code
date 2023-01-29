string = "3113322113"

for loop in range(50):
  output = ""
  count = 1
  digit = string[0]
  for i in range(1, len(string)):
    if string[i] == digit:
      count += 1
    else:
      output += str(count) + digit
      digit = string[i]
      count = 1

  output += str(count) + digit
  #print(loop, output)
  string = output

print(len(output))