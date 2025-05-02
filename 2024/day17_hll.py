"""
2 4	B = A % 8
1 1	B = B ^ 1
7 5	C = A // 2 ** B
0 3	A = A // 2 ** 3
1 4	B = B ^ 4
4 4	B = B ^ C
5 5	output B % 8
3 0	jnz A -> 0
"""

# A = 30_886_132
# A = 35_000_000_000_000
# A = 280_000_000_000_000

found = False
program = "2,4,1,1,7,5,0,3,1,4,4,4,5,5,3,0"
for A_start in range(35_000_000_000_000, 280_000_000_000_000):
    if A_start % 1_000_000 == 0:
        print(f"A_start: {A_start:_}")
    A = A_start
    B = 0
    C = 0
    output = []
    finished = False
    while not finished:
        B = (A % 8) ^ 1
        C = A // 2**B
        A //= 8
        B = (B ^ 4) ^ C
        output.append(str(B % 8))
        if A == 0 or not program.startswith(",".join(output)):
            # print(A_start, "->", ",".join(output))
            finished = True
    if ",".join(output) == program:
        found = True

print("Part 2:", A_start)

# 134_999_999 too low
