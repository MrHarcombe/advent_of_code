package day6_test

import (
	"advent_of_code/2024.go/day6"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day6TestData = `....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`

func TestDay6(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 41
	const expected2 = 6

	var part1, part2 = day6.Solution(loader.LoadInput(Day6TestData))
	if part1 != expected1 {
		t.Fatalf("Day 6 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 6 Part 2 expected %d, got %d", expected2, part2)
	}
}
