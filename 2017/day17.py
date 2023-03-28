from collections import deque

test = 3
actual = 367
jumps = actual

for steps in (1000, 10000, 100000, 1000000, 10000000, 50000000):
    buffer = deque([0])
    buffer_len = 1
    position = 0
    # for add in range(1,2018):
    for add in range(1,steps+1):
        position += jumps
        position %= buffer_len

        # zero is always at position 0
        # so don't keep inserting, as only need the value
        # at position 1, but do need to remember how many
        # values would have been inserted (to mod by)
        if position < 2:
            buffer.insert(position+1, add)
        position += 1
        buffer_len += 1

    # print(buffer[buffer.index(2017)+1])
    # print(buffer[buffer.index(0)+1])
    print(buffer.index(0), buffer[buffer.index(0)+1])
