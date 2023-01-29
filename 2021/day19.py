from collections import defaultdict
from functools import reduce
from itertools import permutations
import io
import numpy as np

test = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''


# def plot_grid(data):
#     grid = np.zeros((1000,1000,1000), dtype=int)
#     for x,y,z in data:
#         grid[(x,y,z)] = 1
#     return grid


def manhattan_distances(beacon, others):
    distances = []
    for other in others:
        distance = sum(abs(val1-val2) for val1, val2 in zip(beacon, other))
        # print('from:', beacon, 'to:', other, 'distance:', distance)
        distances.append(distance)
    return distances


def manhattan_distance(beacon, other):
    distance = sum(abs(val1-val2) for val1, val2 in zip(beacon, other))
    # print('from:', beacon, 'to:', other, 'distance:', distance)
    return distance


def transmute_sensor_coords():
	yield lambda p: (-p[0], p[1], -p[2])
	yield lambda p: (-p[1], p[2], -p[0])
	yield lambda p: (-p[2], p[0], -p[1])
	yield lambda p: (-p[2], p[1], p[0])
	yield lambda p: (-p[1], p[0], p[2])
	yield lambda p: (-p[0], p[2], p[1])

	yield lambda p: (-p[0], -p[1], p[2])
	yield lambda p: (-p[1], -p[2], p[0])
	yield lambda p: (-p[2], -p[0], p[1])
	yield lambda p: (-p[2], -p[1], -p[0])
	yield lambda p: (-p[1], -p[0], -p[2])
	yield lambda p: (-p[0], -p[2], -p[1])

	yield lambda p: (p[0], p[1], p[2])
	yield lambda p: (p[1], p[2], p[0])
	yield lambda p: (p[2], p[0], p[1])
	yield lambda p: (p[2], p[1], -p[0])
	yield lambda p: (p[1], p[0], -p[2])
	yield lambda p: (p[0], p[2], -p[1])

	yield lambda p: (p[0], -p[1], -p[2])
	yield lambda p: (p[1], -p[2], -p[0])
	yield lambda p: (p[2], -p[0], -p[1])
	yield lambda p: (p[2], -p[1], p[0])
	yield lambda p: (p[1], -p[0], p[2])
	yield lambda p: (p[0], -p[2], p[1])

'''
	yield lambda p: (-p[0], p[1], p[2])
	yield lambda p: (-p[0], p[2], p[1])
	yield lambda p: (p[1], -p[0], p[2])
	yield lambda p: (p[1], p[2], -p[0])
	yield lambda p: (p[2], -p[0], p[1])
	yield lambda p: (p[2], p[1], -p[0])

	yield lambda p: (p[0], -p[1], p[2])
	yield lambda p: (p[0], p[2], -p[1])
	yield lambda p: (-p[1], p[0], p[2])
	yield lambda p: (-p[1], p[2], p[0])
	yield lambda p: (p[2], p[0], -p[1])
	yield lambda p: (p[2], -p[1], p[0])

	yield lambda p: (p[0], p[1], p[2])
	yield lambda p: (p[0], p[2], p[1])
	yield lambda p: (p[1], p[0], p[2])
	yield lambda p: (p[1], p[2], p[0])
	yield lambda p: (p[2], p[0], p[1])
	yield lambda p: (p[2], p[1], p[0])

	yield lambda p: (p[0], p[1], -p[2])
	yield lambda p: (p[0], -p[2], p[1])
	yield lambda p: (p[1], p[0], -p[2])
	yield lambda p: (p[1], -p[2], p[0])
	yield lambda p: (-p[2], p[0], p[1])
	yield lambda p: (-p[2], p[1], p[0])

	yield lambda p: (p[0], -p[1], -p[2])
	yield lambda p: (p[0], -p[2], -p[1])
	yield lambda p: (-p[1], p[0], -p[2])
	yield lambda p: (-p[1], -p[2], p[0])
	yield lambda p: (-p[2], p[0], -p[1])
	yield lambda p: (-p[2], -p[1], p[0])

	yield lambda p: (-p[0], -p[1], -p[2])
	yield lambda p: (-p[0], -p[2], -p[1])
	yield lambda p: (-p[1], -p[0], -p[2])
	yield lambda p: (-p[1], -p[2], -p[0])
	yield lambda p: (-p[2], -p[0], -p[1])
	yield lambda p: (-p[2], -p[1], -p[0])

	yield lambda p: (-p[0], -p[1], p[2])
	yield lambda p: (-p[0], p[2], -p[1])
	yield lambda p: (-p[1], -p[0], p[2])
	yield lambda p: (-p[1], p[2], -p[0])
	yield lambda p: (p[2], -p[0], -p[1])
	yield lambda p: (p[2], -p[1], -p[0])

	yield lambda p: (-p[0], p[1], -p[2])
	yield lambda p: (-p[0], -p[2], p[1])
	yield lambda p: (p[1], -p[0], -p[2])
	yield lambda p: (p[1], -p[2], -p[0])
	yield lambda p: (-p[2], -p[0], p[1])
	yield lambda p: (-p[2], p[1], -p[0])
'''


scanner_points = {}
new_scanner_points = {}
scanner_distances = {}
# grids = {}

with io.StringIO(test) as file:
    scanner_number = None
    scanner = []

    for line in file:
        if len(line.strip()) == 0:
            if scanner_number != None:
                scanner_points[scanner_number] = scanner
                # grids[scanner_number] = plot_grid(scanner)
                scanner = []
            else:
                print('Storing without a number', len(scanner))
            continue

        elif '---' in line:
            scanner_number = int(line.split()[2])

        else:
            scanner.append(tuple(int(n) for n in line.strip().split(',')))

    if scanner_number not in scanner_points and len(scanner) > 0:
        scanner_points[scanner_number] = scanner
        # grids[scanner_number] = plot_grid(scanner)

print(scanner_points.keys())

# for scanner in scanner_points:
#     distances = {}
#     beacons = scanner_points[scanner]
#     if scanner == 0:
#         for i, point in enumerate(beacons):
#             distances[tuple(point)] = (None, manhattan_distances(point, beacons))
#         scanner_distances[scanner] = distances
#     else:
#         for func in transmute_sensor_coords():
#             new_points = list(map(func, beacons))
#             for i, point in enumerate(new_points):
#                 distances[point] = (func, manhattan_distances(point, new_points))
#         scanner_distances[scanner] = distances

all_matches = defaultdict(list)

offsets_from_0 = { 0 : (0, 0, 0) }
new_scanner_points[0] = scanner_points[0]
overall_points = set(scanner_points[0])

for scanner1, scanner2 in permutations(scanner_points, 2):
    if (scanner2,scanner1) in all_matches:
        continue

    # print('comparing:', scanner1, scanner2)
    # s1_points = scanner_distances[scanner1]
    # s2_points = scanner_distances[scanner2]

    for s1_point in scanner_points[scanner1]:
        s1_distances = manhattan_distances(s1_point, scanner_points[scanner1])
        s1_set = set(s1_distances)

        s2_points = scanner_points[scanner2]
        for s2_point in scanner_points[scanner2]:
            s2_distances = manhattan_distances(s2_point, s2_points)
            intersect = s1_set.intersection(s2_distances)
            if len(intersect) > 9:
                all_matches[(scanner1, scanner2)].append((s1_point, s2_point))

    match_pairs = all_matches[(scanner1, scanner2)]
    if len(match_pairs) == 12:
        for func in transmute_sensor_coords():
            distances = []
            for s1p, s2p in match_pairs:
                distances.append(manhattan_distance(s1p, func(s2p)))

            if len(set(distances)) == 1:
                match_p1 = 0
                match_p2 = 1

                if scanner1 not in new_scanner_points:
                    scanner1, scanner2 = scanner2, scanner1
                    match_p1, match_p2 = match_p2, match_p1

                cs1p = new_scanner_points[scanner1]
                os2p = scanner_points[scanner2]

                s1c = scanner_points[scanner1].index(match_pairs[0][match_p1])
                s2c = os2p.index(match_pairs[0][match_p2])

                ##
                # generate the offset?
                #
                t2p0 = func(os2p[s2c])

                offset = offsets_from_0[scanner1]
                offset_x = cs1p[s1c][0] - t2p0[0]
                offset_y = cs1p[s1c][1] - t2p0[1]
                offset_z = cs1p[s1c][2] - t2p0[2]
                offsets_from_0[scanner2] = (offset_x, offset_y, offset_z)
                print(offsets_from_0)

                points = scanner_points[scanner2]
                new_points = []
                for point in points:
                    new_point = func(point)
                    new_point = (new_point[0] + offset_x, new_point[1] + offset_y, new_point[2] + offset_z)
                    new_points.append(new_point)
                    overall_points.add(new_point)

                new_scanner_points[scanner2] = new_points
                break

print(len(overall_points))