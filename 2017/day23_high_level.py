from time import time

# a = 1
upper = lower = 84
# d = e = f = h = 0

# if a != 0:
lower = lower * 100 + 100000
upper = lower + 17000

### first pass into Python

# while True:
#     f = 1
#     d = 2
# 
#     while True:
#         e = 2
# 
#         while True:
#             if d * e == b:
#                 f = 0
# 
#             e += 1
#             if e == b: break
# 
#         d += 1
#         if d == b: break
# 
#     if f == 0:
#         h += 1
# 
#     if b == c: break
# 
#     b -= 17

def is_prime(num):
    for n in range(2,int(num ** 0.5)+1):
        if num % n == 0:
            return False

    return True

b = d = e = f = h = 0

for b in range(lower, upper+1, 17):
    f = 1
    ### second pass into Python
    #
    # for d in range(2, b+1):
    #     for e in range(2, b+1):
    #         if d * e == b:
    #             f = 0
    #             break
    #         
    #     if f == 0:
    #         break
    if not is_prime(b):
        f = 0

    if f == 0:
        h += 1

start = time()
# print(f"{a=}")
print(f"{lower=}")
print(f"{upper=}")
print(f"{b=}")
print(f"{d=}")
print(f"{e=}")
print(f"{f=}")
print(f"{h=}")
print("Elapsed:", time() - start)