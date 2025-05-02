package day8_test

import (
	"advent_of_code/2024.go/day8"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day8TestData = `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`

func TestDay8(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 14
	const expected2 = 34

	var part1, part2 = day8.Solution(loader.LoadInput(Day8TestData))
	if part1 != expected1 {
		t.Fatalf("Day 8 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 8 Part 2 expected %d, got %d", expected2, part2)
	}
}
