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

test = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

server_rack = {}

def bfs(server_rack, start, end, contains = None):
    queue = [[[start], []]]
    
    while len(queue):
        current_path, visited = queue.pop(0)
        current = current_path[-1]
        visited.append(current)

        if current == end:
            if contains is None:
                yield 1
            elif all(c in current_path for c in contains):
                yield 1

        else:
            for connected in server_rack[current]:
                next_path = current_path + [connected]
                if connected not in visited:
                    queue.append([next_path, visited])


# with StringIO(test) as data:
with open("input11.txt") as data:
    for line in data:
        device, outputs = line.strip().split(": ")
        server_rack[device] = outputs.split()

print("Part 1:", sum(bfs(server_rack, "you", "out")))

svr_dac = sum(bfs(server_rack, "svr", "dac"))
print("Done")
dac_fft = sum(bfs(server_rack, "dac", "fft"))
print("Done")
fft_out = sum(bfs(server_rack, "fft", "out"))
print("Done")

svr_fft = sum(bfs(server_rack, "svr", "fft"))
print("Done")
fft_dac = sum(bfs(server_rack, "fft", "dac"))
print("Done")
dac_out = sum(bfs(server_rack, "dac", "out"))
print("Done")

print("Part 2:", svr_dac*dac_fft*fft_out + svr_fft*fft_dac*dac_out)
