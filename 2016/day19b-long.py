#group = [n for n in range(1,6)]
group = [n for n in range(1, 3014604)]
#print(group)

current_elf = 0
while len(group) > 1:
    stolen = (current_elf + len(group) // 2) % len(group)
    # stolen = len(group) // 2
    #print("current_elf:", group[current_elf], "stealing:", group[stolen])

    group = group[:stolen] + group[stolen+1:]
    # print(group)
    
    current_elf += 1
    if current_elf > len(group) - 1:
        current_elf = 0

print(group)

