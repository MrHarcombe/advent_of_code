import hashlib

prefix = "abbhdwsy"
#prefix = "abc" # test
start = 0
password = ["_" for n in range(8)]

while len(password) < 8:
    m = hashlib.md5(f"{prefix}{start}".encode("utf8"))
    digest = m.hexdigest()
    if digest.startswith("00000"):
        print(start,digest)
        password.append(digest[5])
    start += 1

print("".join(password))

