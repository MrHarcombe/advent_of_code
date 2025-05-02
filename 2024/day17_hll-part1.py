from time import time

begin = time()
A = 30_886_132
# A = 35_000_000_000_000
# A = 280_000_000_000_000
A = 19_064_863_836_961_074
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
    if A == 0:
        finished = True

print(",".join(output))
print("Elapsed:", time() - begin)
