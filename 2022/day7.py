from io import StringIO
from collections import defaultdict

test = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def parse_line(line):
    global dirs, current
    
    command = line.split()
    # print(command, current)
    
    if command[0] == "$" and command[1] == "cd":
        if command[2] == "/":
            current = ""
        elif command[2] == "..":
            current = current[:current.rindex("/")]
        else:
            current += "/" + command[2]

        if current not in dirs:
            dirs[current] = 0

        # print("cd:", current)

    elif command[0] != "$" and command[0] != "dir":
        size = int(command[0])
        for d in dirs.keys():
            # print("checking for file in:", current, d)
            if current.startswith(d):
                # print("adding")
                dirs[d] += size

dirs = defaultdict(int)
current = ""

with StringIO(test) as f:
# with open("input7.txt") as f:
    for line in f:
        parse_line(line.strip())
        
print("part a:", sum([value for value in dirs.values() if value <= 100000]))

unused = 70000000
free = unused - dirs[""]
needed = 30000000 - free
possibles = [item for item in dirs.items() if item[1] > needed]
print("part b:", min(possibles, key=lambda i:i[1]))
