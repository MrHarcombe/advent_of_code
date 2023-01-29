group = [n for n in range(1,11)]
#group = [n for n in range(1, 3014604)]
#print(group)

# current_elf = 0
while len(group) > 2:
    # stolen = (current_elf + len(group) // 2) % len(group)
    stolen = len(group) // 2
    # print("current_elf:", group[current_elf], "stealing:", group[stolen])

    group = group[stolen:] + group[:stolen]
    print(group)
    
    if len(group) % 2 == 0:
        keep_index = 2
        # starting from index 1, skip 2, then 1 to the end
        
    else:
        keep_index = 1
        # starting from index 2, skip 2, then 1 to the end

    new_group = []
    two = True
    while keep_index < len(group):
        new_group.append(group[keep_index])
        if two:
            keep_index += 3
            two = False
        else:
            keep_index += 2
            two = True

    print(new_group)
    group = sorted(new_group)
    
#     current_elf += 1
#     if current_elf > len(group):
#         current_elf = 0

print(group)
