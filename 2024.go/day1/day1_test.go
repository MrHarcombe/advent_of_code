package day1_test

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day1TestData = `3   4
4   3
2   5
1   3
3   9
3   3`

func TestDay1(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 11
	const expected2 = 31

	var part1, part2 = day1.Solution(loader.LoadInput(Day1TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}
