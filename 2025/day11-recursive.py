from functools import cache
from io import StringIO


test = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

# test = """svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out"""


server_rack= {}

@cache
def bfs_recursive(node, end, contains = tuple()):
    if node == end:
        return len(contains) == 0

    contains = tuple(c for c in contains if c != node)
    return sum(bfs_recursive(child, end, contains) for child in server_rack[node])

# with StringIO(test) as data:
with open("input11.txt") as data:
    for line in data:
        device, outputs = line.strip().split(": ")
        server_rack[device] = tuple(outputs.split())

print("Part 1:", bfs_recursive("you", "out"))
print("Part 2:", bfs_recursive("svr", "out", ("fft", "dac")))
