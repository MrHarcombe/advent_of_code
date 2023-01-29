from hashlib import md5
import re

key_counter = 0
keycount = 0

candidate = re.compile(r"(?P<first>.)(?P=first){2}")

prefix = "abc"
prefix = "jlmsuwbz"

while keycount < 64:
    match = None
    while match == None:
        possible = md5(f"{prefix}{key_counter}".encode()).hexdigest()
        for n in range(2016):
            possible = md5(possible.encode()).hexdigest()
        # print(possible)

        match = candidate.search(possible)
        
        if match != None:
            # print(key_counter, match, match.group(1))
            
            check = re.compile(r"(?P<check>"+match.group(1)+r"){5}")
            for check_counter in range(key_counter+1, key_counter+1001):
                check_possible = md5(f"{prefix}{check_counter}".encode()).hexdigest()
                for n in range(2016):
                    check_possible = md5(check_possible.encode()).hexdigest()
                # print(check_possible)
                
                check_match = check.search(check_possible)
                
                if check_match != None:
                    print("found key", key_counter, possible, check_counter, check_possible)
                    keycount += 1
                    break
            else:            
                match = None

        key_counter += 1
            
