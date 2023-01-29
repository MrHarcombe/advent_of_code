from collections import Counter
from io import StringIO

def parse_room(room):
    name_and_sector, checksum = room[:-1].split("[")
    last_dash = name_and_sector.rfind("-")
    name = name_and_sector[:last_dash].replace("-","")
    sector = name_and_sector[last_dash+1:]
    
    # print(name, sector, checksum)
    
    counts = Counter(name)
    # print(counts)
    previous = 0
    generated_checksum = []
    tiebreak = []
    for ch, n in counts.most_common():
        if n == previous:
            tiebreak.append(ch)
        else:
            previous = n
            generated_checksum.append("".join(sorted(tiebreak)))
            tiebreak = [ch]
    generated_checksum.append("".join(sorted(tiebreak)))
    # print(generated_checksum)
    
    if checksum == "".join(generated_checksum)[:5]:
        return int(sector)
    
    return 0

def decrypt_room(room):
    name_and_sector, checksum = room[:-1].split("[")
    last_dash = name_and_sector.rfind("-")
    name = name_and_sector[:last_dash].replace("-","")
    sector = name_and_sector[last_dash+1:]

    offset = int(sector) % 26
    
    new_name = []
    for ch in name:
        if ch == "-":
            new_name.append(" ")
        else:
            ch = chr((((ord(ch) - ord("a")) + offset) % 26) + ord("a"))

        new_name.append(ch)
        
    return "".join(new_name)

# YYYN -> 1514
test_data = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

total = 0
#with StringIO(test_data) as f:
with open("input4.txt") as f:
    for line in f:
        sector = parse_room(line.strip())
        if sector > 0:
            decrypt = decrypt_room(line.strip()).lower()
            if "north" in decrypt and "pole" in decrypt:
                print(decrypt, sector)