package day2_test

import (
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day2TestData = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

func TestDay2(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 2
	const expected2 = 4

	var part1, part2 = day2.Solution(loader.LoadInput(Day2TestData))
	if part1 != expected1 {
		t.Fatalf("Day 2 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 2 Part 2 expected %d, got %d", expected2, part2)
	}
}
