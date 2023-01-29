import hashlib

prefix = "abbhdwsy"
#prefix = "abc" # test
start = 0
#a password = []
password = ["_" for n in range(8)]

while "_" in password:
    m = hashlib.md5(f"{prefix}{start}".encode("utf8"))
    digest = m.hexdigest()
    if digest.startswith("00000"):
        #a print(start,digest)
        #a password.append(digest[5])
        if int(digest[5],16) in range(8) and password[int(digest[5],16)] == "_":
            password[int(digest[5],16)] = digest[6]
        print("".join(password))
    start += 1
