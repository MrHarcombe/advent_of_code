import re
import io

def parse_ipv7(address):
    outer = []
    hypernet = []
    
    next_bracket = address.find("[")
    while next_bracket != -1:
        outer.append(address[:next_bracket])
        address = address[next_bracket+1:]
        next_bracket = address.find("]")
        hypernet.append(address[:next_bracket])
        address = address[next_bracket+1:]
        next_bracket = address.find("[")
    outer.append(address)
    
    return " ".join(outer), " ".join(hypernet)

def has_abba(ip):
    abba = r"(?P<first>.)(?!\1)(?P<second>.)(?P=second)(?P=first)"
    results = re.search(abba, ip)
    return results != None

def has_aba_bab(outer, inner):
    aba = re.compile(r"(?P<first>.)(?!\1)(?P<second>.)(?P=first)")
    for i in range(len(outer)):
        match = aba.match(outer, i)
        if match != None:
            # print(match.groups())
            a = match.group(1)
            b = match.group(2)
            
            bab = r"(?P<first>["+b+r"])(?!\1)(?P<second>["+a+r"])(?P=first)"
            match = re.search(bab, inner)
            if match != None:
                # print("Has aba bab")
                return True
    
    return False

# YNNY
test1 = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""

test2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""

test = test2

total = 0
with open("input7.txt") as f:
# with io.StringIO(test) as f:
    for line in f:
        outer, hypernet = parse_ipv7(line.strip())
        # if has_abba(outer) and not has_abba(hypernet):
        if has_aba_bab(outer, hypernet):
            # print(line.strip(), "supports TLS")
            total += 1
        else:
            # print(test, "does not support TLS")
            pass
        
print(total)
