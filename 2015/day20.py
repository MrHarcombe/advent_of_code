from math import floor

target = 29000000

def factors(n):
    stop = floor(n ** 0.5)
    factors = []
    for i in range(1, stop+1):
        if n % i == 0:
            factors.append(n // i)
            if i not in factors:
                factors.append(i)
    return factors

presents = 0
house = 705000
while presents <= target:
    f = factors(house)
    presents = sum([fac * 11 for fac in f if house <= 50 * fac])
    print(house, presents, [fac for fac in f if house <= 50 * fac])
    house += 1

print(house)