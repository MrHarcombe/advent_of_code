def check_a(a, check_digit):
    return (((a % 8) ^ 5) ^ (a >> ((a % 8) ^ 1)) % 8) == check_digit


program = "2,4,1,1,7,5,0,3,1,4,4,4,5,5,3,0"
check_digits = list(map(int, reversed(program.split(","))))
possibles = []

queue = [(num, 0) for num in range(2**10) if check_a(num, 0)]
while len(queue) > 0:
    num, pos = queue.pop(0)

    if pos + 1 == len(check_digits):
        possibles.append(num)
        continue

    for new_a in range(num * 8, num * 8 + 8):
        if check_a(new_a, check_digits[pos + 1]):
            queue.append((new_a, pos + 1))

print("Part 2:", min(possibles))
print("Note:", len(possibles), "possibles")
