test = "flqrgnkx"
actual = "vbqugkhl"

def knot_hash(kh_input):
    lengths = [ord(n) for n in kh_input] + [17, 31, 73, 47, 23]
    loop = [n for n in range(256)]

    skip = 0
    position = 0

    for rnd in range(64):
        for step in lengths:
            sub = []
            for n in range(step):
                sub.append(loop[(position + n) % len(loop)])
            for n in range(step):
                loop[(position + n) % len(loop)] = sub.pop()
            
            position = (position + step + skip) % len(loop)
            skip += 1

    dense = []
    for i in range(0, len(loop), 16):
        value = loop[i]
        for j in range(i+1, i+16):
            value ^= loop[j]
        dense.append(f"{value:02x}")

    return "".join(dense)

prefix = actual
# for row in range(128):
#     hash_row = f"{prefix}-{row}"
#     value = int(knot_hash(hash_row), 16)
print(sum([f"{int(knot_hash(prefix+'-'+str(row)), 16):0128b}".count("1") for row in range(128)]))
