numbers = []

with open("input.txt") as part1:
  number = part1.readline()
  while number != '':
    numbers.append(int(number))
    number = part1.readline()

#print(numbers)
done = False
for i in range(len(numbers)):
  if done: break
  for j in range(1, len(numbers)):
    if done: break
    for k in range(2, len(numbers)):
      if numbers[i]+numbers[j]+numbers[k] == 2020:
        print(f"!!! {numbers[i]*numbers[j]*numbers[k]} !!!")
        done = True
