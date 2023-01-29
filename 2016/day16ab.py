from io import StringIO

test = "10000"

def dragon(data, minimum_length):
    while len(data) < minimum_length:
        a = list(data)
        b = a[::-1]
        for i in range(len(b)):
            b[i] = "0" if b[i] == "1" else "1"

        data = "".join(a) + "0" + "".join(b)
    
    return data

def checksum(data, checksum_length):
    checksum_data = list(data[:checksum_length])
    while len(checksum_data) % 2 == 0:
        checksum_bits = []
        for i in range(0, len(checksum_data), 2):
            if checksum_data[i] == checksum_data[i+1]:
                checksum_bits.append("1")
            else:
                checksum_bits.append("0")

        checksum_data = "".join(checksum_bits)

    return checksum_data

assert(dragon(test, 20) == "10000011110010000111110")
assert(checksum(dragon(test, 20), 20) == "01100")

print(checksum(dragon("10111011111001111", 272), 272))
print(checksum(dragon("10111011111001111", 35651584), 35651584))

