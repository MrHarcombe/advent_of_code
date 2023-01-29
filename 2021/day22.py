import io
import numpy as np

test_1 = '''on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10'''
test_2 = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''
test_3 = '''on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507'''

test = test_3

cube_commands = []

# with io.StringIO(test) as inputs:
with open('input22.txt') as inputs:
    for line in inputs:
        toggle, command = line.strip().split()
        cubes = tuple([tuple([int(n) for n in axis.split('=')[1].split('..')]) for axis in command.split(',')])
        # print(cubes)
        cube_commands.append((toggle, cubes))

print(cube_commands)

# min_x, min_y, min_z = 0,0,0
# max_x, max_y, max_z = 0,0,0
# for cmd in cube_commands:
#     x,y,z = cmd[1]

#     min_x = min(x[0], min_x)
#     min_y = min(y[0], min_y)
#     min_z = min(z[0], min_z)

#     max_x = max(x[1], max_x)
#     max_y = max(y[1], max_y)
#     max_z = max(z[1], max_z)

# print('x:', min_x, max_x)
# print('y:', min_y, max_y)
# print('z:', min_z, max_z)
# print('volume:', (max_x - min_x) * (max_y - min_y) * (max_z - min_z))

def initialisation():
    volume = {}

    for cmd in cube_commands:
        x,y,z = cmd[1]
        for z_run in range(max(-50,z[0]), min(50,z[1])+1):
            for y_run in range(max(-50,y[0]), min(50,y[1])+1):
                for x_run in range(max(-50,x[0]), min(50,x[1])+1):
                    volume[(x_run,y_run,z_run)] = ((1).to_bytes(1,byteorder='big') if cmd[0] == 'on' else (0).to_bytes(1,byteorder='big'))

    # print(volume)
    print('init:', sum([int.from_bytes(b, byteorder='big') for b in volume.values()]))

# def reboot():
#     volume = {}

#     for i, cmd in enumerate(cube_commands):
#         min_x, min_y, min_z = float('inf'),float('inf'),float('inf')
#         max_x, max_y, max_z = 0,0,0

#         x,y,z = cmd[1]

#         min_x = min(x[0], min_x)
#         min_y = min(y[0], min_y)
#         min_z = min(z[0], min_z)

#         max_x = max(x[1], max_x)
#         max_y = max(y[1], max_y)
#         max_z = max(z[1], max_z)

#         x_range = ((max_x - min_x) + 1)
#         y_range = ((max_y  - min_y) + 1)
#         z_range = ((max_z - min_z) + 1)

#         print(f'turning {cmd[0]} cube {i} of {len(cube_commands)}, size {x_range*y_range*z_range}')

#         cube_volume = x_range * y_range * z_range
#         for pos in range(cube_volume+1):
#             x_pos = (pos % x_range) + min_x
#             y_pos = ((pos % (x_range * y_range)) // x_range) + min_y
#             z_pos = (pos // (x_range * y_range)) + min_z

#             # print(f'pos: {pos}, x: {x_pos}, y: {y_pos}, z: {z_pos}')
#             if cmd[0] == 'on':
#                 volume[(x_pos,y_pos,z_pos)] = (1).to_bytes(1,byteorder='big')
#             elif (x_pos,y_pos,z_pos) in volume:
#                 del volume[(x_pos,y_pos,z_pos)]

#     # print(volume)
#     print('reboot:', sum([int.from_bytes(b, byteorder='big') for b in volume.values()]))


def split_cubes(cube1, cube2):
    x1,y1,z1 = cube1[1]
    x2,y2,z2 = cube2[1]

    c1_min_x,c1_max_x = x1
    c1_min_y,c1_max_y = y1
    c1_min_z,c1_max_z = z1

    c2_min_x,c2_max_x = x2
    c2_min_y,c2_max_y = y2
    c2_min_z,c2_max_z = z2

    # no overlap, keep both
    if (c1_min_x > c2_max_x or c1_max_x < c2_min_x or
        c1_min_y > c2_max_y or c1_max_y < c2_min_y or
        c1_min_z > c2_max_z or c1_max_z < c2_min_z):
        return { cube1 : 0, cube2 : 0 }

    # carve them up and return constituent parts

    # first, consider the x-axis
    # cube1 starts to the "left" of cube2
    if c1_min_x < c2_min_x:
        # cube1 is fully enclosed within cube2 on the x-axis
        if c1_max_x > c2_max_x:
            cube1_a = (cube1[0], ((c1_min_x, c2_min_x - 1), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))
            cube1_b = (cube1[0], ((c2_min_x, c2_max_x), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))
            cube1_c = (cube1[0], ((c2_max_x + 1, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))

            left = { cube1_a : 0, cube1_c : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

        # cube1 ends short of the "right" of cube2
        else:
            cube1_a = (cube1[0], ((c1_min_x, c2_min_x - 1), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))
            cube1_b = (cube1[0], ((c2_min_x, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))

            left = { cube1_a : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

    # else "left" side of cube1 overlaps inside "right" side of cube2
    elif c1_max_x > c2_max_x:
        cube1_a = (cube1[0], ((c1_min_x, c2_max_x), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))
        cube1_b = (cube1[0], ((c2_max_x + 1, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c1_max_z)))

        left = { cube1_b : 0 }
        return { **left, **split_cubes(cube1_a, cube2) }

    # next, consider the y-axis
    # cube1 starts "below" cube2
    elif c1_min_y < c2_min_y:
        # cube2 is fully enclosed within cube1 on the y-axis
        if c1_max_y > c2_max_y:
            cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c2_min_y - 1), (c1_min_z, c1_max_z)))
            cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c2_min_y, c2_max_y), (c1_min_z, c1_max_z)))
            cube1_c = (cube1[0], ((c1_min_x, c1_max_x), (c2_max_y + 1, c1_max_y), (c1_min_z, c1_max_z)))
            
            left = { cube1_a : 0, cube1_c : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

        # "top" of cube1 overlaps "bottom" of cube2
        else: 
            cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c2_min_y - 1), (c1_min_z, c1_max_z)))
            cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c2_min_y, c1_max_y), (c1_min_z, c1_max_z)))

            left = { cube1_a : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

    # else "bottom" of cube1 overlaps inside "top" of cube2
    elif c1_max_y > c2_max_y: 
        cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c2_max_y), (c1_min_z, c1_max_z)))
        cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c2_max_y + 1, c1_max_y), (c1_min_z, c1_max_z)))

        left = { cube1_b : 0 }
        return { **left, **split_cubes(cube1_a, cube2) }

    # finally, consider the z-axis
    # cube1 starts "behind" cube2
    elif c1_min_z < c2_min_z:
        # cube2 is fully enclosed within cube1 on the z axis
        if c1_max_z > c2_max_z:
            cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c2_min_z - 1)))
            cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c2_min_z, c2_max_z)))
            cube1_c = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c2_max_z + 1, c1_max_z)))

            left = { cube1_a : 0, cube1_c : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

        else: # "far" side of cube1 overlaps "near" side of cube2
            cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c2_min_z - 1)))
            cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c2_min_z, c1_max_z)))

            left = { cube1_a : 0 }
            return { **left, **split_cubes(cube1_b, cube2) }

    # else "near" side of cube1 overlaps within "far" side of cube2
    elif c1_max_z > c2_max_z:
        cube1_a = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c1_min_z, c2_max_z)))
        cube1_b = (cube1[0], ((c1_min_x, c1_max_x), (c1_min_y, c1_max_y), (c2_max_z + 1, c1_max_z)))

        left = { cube1_b : 0 }
        return { **left, **split_cubes(cube1_a, cube2) }

    # cube2 completely encloses cube1
    return { cube2 : 0 }


def volume(cube):
    x,y,z = cube[1]

    min_x, max_x = x
    min_y, max_y = y
    min_z, max_z = z

    # print('x:', min_x, max_x)
    # print('y:', min_y, max_y)
    # print('z:', min_z, max_z)
    # print('volume:', (max_x + 1 - min_x) * (max_y + 1 - min_y) * (max_z + 1 - min_z))

    return (max_x + 1 - min_x) * (max_y + 1 - min_y) * (max_z + 1 - min_z)


def reboot():
    all_cubes = {cube_commands[0]}
    for command in cube_commands[1:]:
        new_cubes = {}

        # consider everything we have split, to date
        for cube in all_cubes:
            new_cubes = { **new_cubes, **split_cubes(cube, command) }

        # start from there, next time
        all_cubes = { cube for cube in new_cubes if cube[0] == 'on' }

    total_volume = 0
    for cube in all_cubes:
        total_volume += volume(cube)
    print('reboot:', total_volume)

initialisation()
reboot()