valid = 0

with open("input.txt") as f:
  password = f.readline()
  while password != '':
    rules = password.split()
    occurs = rules[0]
    letter = rules[1].split(':')[0]
    password = rules[2]
    print(occurs, letter, password)

    low,high = map(int, occurs.split('-'))
    print(low,high)

    count = password.count(letter)

    if low <= count <= high:
      valid +=1
    
    password = f.readline()

print(valid)