directions = {
    0: (0, -1),
    1: (1, -1),
    2: (1, 0),
    3: (1, 1),
    4: (0, 1),
    5: (-1, 1),
    6: (-1, 0),
    7: (-1, -1),
}

for diagonal in (1, 3, 5, 7):
    dix, diy = directions[diagonal]
    adjacent = tuple(
        (directions[d][0], directions[d][1])
        for d in ((diagonal - 1) % 8, (diagonal + 1) % 8)
    )

    print(diagonal, adjacent)
