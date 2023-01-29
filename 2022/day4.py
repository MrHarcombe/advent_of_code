from io import StringIO

test="""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

count_a = 0
count_b = 0
# with StringIO(test) as f:
with open("input4.txt") as f:
    for line in f:
        elf1,elf2 = line.strip().split(",")
        e1s,e1e = [int(n) for n in elf1.split("-")]
        e2s,e2e = [int(n) for n in elf2.split("-")]
        
#         print(e1s,"-",e1e,"/",e2s,"-",e2e, end=" ")
        if e1s>=e2s and e1e<=e2e or e2s>=e1s and e2e<=e1e:
            count_a += 1
#             print(True, end=" ")
#         else:
#             print(False, end=" ")
            
        if e1s <= e2s and e1e >= e2s or e1s >= e2s and e1s <= e2e and e1e >= e2e or e2s <= e1s and e2e >= e1s or e2s >= e1s and e2s <= e1e and e2e >= e1e:
            count_b += 1
#             print(True, end=" ")
#         else:
#             print(False, end=" ")

#         print()

print(count_a, count_b)
