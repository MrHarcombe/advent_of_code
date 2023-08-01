from io import StringIO
from collections import Counter, defaultdict

test = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""

test2 = """p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>"""

def tick_and_find_closest(particles):
    closest = float("inf")
    closest_p = -1

    for p in range(len(particles)):
        xp, yp, zp = particles[p][0]
        xv, yv, zv = particles[p][1]
        xa, ya, za = particles[p][2]

        xv += xa
        yv += ya
        zv += za
        particles[p][1] = [xv, yv, zv]

        xp += xv
        yp += yv
        zp += zv
        particles[p][0] = [xp, yp, zp]

        distance = abs(xp) + abs(yp) + abs(zp)
        if distance < closest:
            closest = distance
            closest_p = p

    return closest_p

def tick_and_collide(particles):
    endpoints = defaultdict(list)

    for p in range(len(particles)):
        xp, yp, zp = particles[p][0]
        xv, yv, zv = particles[p][1]
        xa, ya, za = particles[p][2]

        xv += xa
        yv += ya
        zv += za
        particles[p][1] = [xv, yv, zv]

        xp += xv
        yp += yv
        zp += zv
        particles[p][0] = [xp, yp, zp]
        endpoints[(xp,yp,zp)].append(p)

    # print(endpoints)
    to_delete = []
    for e in endpoints:
        pl = endpoints[e]
        if len(pl) > 1:
            to_delete += pl

    for p in sorted(to_delete, reverse=True):
        del particles[p]

particles = []
# with StringIO(test2) as data:
with open("input20.txt") as data:
    for line in data:
        p, v, a = line.split(", ")
        p = [int(n) for n in p.split("=<")[1].strip()[:-1].split(",")]
        v = [int(n) for n in v.split("=<")[1].strip()[:-1].split(",")]
        a = [int(n) for n in a.split("=<")[1].strip()[:-1].split(",")]

        particles.append([p, v, a])

counter = Counter()

# for _ in range(5000):
#     closest = tick_and_find_closest(particles)
#     counter[closest] += 1
# print("Part 1:", counter)

for _ in range(1000):
    tick_and_collide(particles)
print("Part 2:", len(particles))
