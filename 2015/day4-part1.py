import hashlib

secret = bytes("bgvyzdsv", "utf8")

suffix = 254570
complete = False

while not complete:
  suffix += 1
  digest = hashlib.md5(secret + bytes(str(suffix), "utf8")).hexdigest()
  # print(suffix,'->',digest)
  complete = digest[:6] == '000000'

print(suffix)
