# gen_a = 65
# gen_b = 8921

gen_a = 277
gen_b = 349

gen_a_factor = 16807
gen_b_factor = 48271

modulo = 2147483647
mask = int("1111111111111111", 2)

judgements = 0

# for i in range(40000000):
for i in range(5000000):
    gen_a *= gen_a_factor
    gen_a %= modulo
    while gen_a % 4 != 0:
        gen_a *= gen_a_factor
        gen_a %= modulo
    # print(gen_a)

    gen_b *= gen_b_factor
    gen_b %= modulo
    while gen_b % 8 != 0:
        gen_b *= gen_b_factor
        gen_b %= modulo
    # print(gen_b)

    if gen_a & mask == gen_b & mask:
        judgements += 1

print(judgements)
