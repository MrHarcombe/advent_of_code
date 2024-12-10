from io import StringIO

test = "12345"
test = "2333133121414131402"


def defrag_p1(disk_map, id_map):
    index = disk_map.pop(0)
    while index < len(id_map):
        count = disk_map.pop(0)
        values = []
        while len(values) < count:
            if id_map[-1] != -1:
                values.append(id_map[-1])
            id_map.pop()
        for ix, id in enumerate(values):
            if index + ix <= len(id_map):
                id_map[index + ix] = id
            else:
                id_map.append(id)

        index += count
        index += disk_map.pop(0)

    # print(disk_map, id_map)
    return id_map


def defrag_p2(disk_map, id_map):
    # disk_index = 0
    # index = disk_map[disk_index]
    move_id = len(disk_map) // 2
    move_count = disk_map[(move_id * 2)]
    empty_count = id_map.count(-1)
    while move_id > 0:
        empty_index = -1
        for _ in range(empty_count):
            empty_index = id_map.index(-1, empty_index + 1)
            if id_map.index(move_id) < empty_index:
                break

            if id_map[empty_index : empty_index + move_count] == [-1] * move_count:
                start = id_map.index(move_id)
                for wipe_index in range(start, start + move_count):
                    id_map[wipe_index] = -1
                for fill_index in range(empty_index, empty_index + move_count):
                    id_map[fill_index] = move_id
                empty_count -= move_count
                break

        move_id -= 1
        move_count = disk_map[(move_id * 2)]

    # print(disk_map, id_map)
    return id_map


# with StringIO(test) as input_data:
with open("input9.txt") as input_data:
    for line in input_data:
        disk_map = list(map(int, list(line.strip())))

        id_map = []
        id = 0
        space = False
        for num in disk_map:
            if not space:
                id_map += [id] * num
                id += 1
            else:
                id_map += [-1] * num
            space = not space

    p1_id_map = defrag_p1(list(disk_map), list(id_map))
    p2_id_map = defrag_p2(list(disk_map), list(id_map))

checksum1 = 0
for i, num in enumerate(p1_id_map):
    checksum1 += i * num

checksum2 = 0
for i, num in enumerate(p2_id_map):
    if num != -1:
        checksum2 += i * num

print("Part 1:", checksum1)
print("Part 2:", checksum2)
