valid = 0

with open("input.txt") as f:
  password = f.readline()
  while password != '':
    rules = password.split()
    occurs = rules[0]
    letter = rules[1].split(':')[0]
    password = rules[2]
    #print(occurs, letter, password)

    low,high = map(int, occurs.split('-'))
    #print(low,high)

    letters = password

    count = (letters[low-1] + letters[high-1]).count(letter)
    print(letters, letter, count)

    if count == 1:
      valid +=1
      print("found one")
    
    password = f.readline()

print(valid)