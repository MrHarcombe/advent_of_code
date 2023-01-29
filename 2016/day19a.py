group = [n for n in range(1, 3014604)]
#print(group)

while len(group) > 1:
    if len(group) % 2 == 1:
        new_group = [group[-1]] + [group[i] for i in range(0, len(group)-1, 2)]
    else:
        new_group = [group[i] for i in range(0, len(group), 2)]

    #print(new_group)
    group = new_group

print(group)