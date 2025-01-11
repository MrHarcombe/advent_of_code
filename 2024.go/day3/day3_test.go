package day3_test

import (
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day3TestData = `xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))`

func TestDay3(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 161
	const expected2 = 48

	var part1, part2 = day3.Solution(loader.LoadInput(Day3TestData))
	if part1 != expected1 {
		t.Fatalf("Day 3 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 3 Part 2 expected %d, got %d", expected2, part2)
	}
}
