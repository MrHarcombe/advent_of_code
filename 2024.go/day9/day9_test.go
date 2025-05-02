package day9_test

import (
	"advent_of_code/2024.go/day9"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day9TestData = `2333133121414131402`

func TestDay9(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 1928
	const expected2 = 2858

	var part1, part2 = day9.Solution(loader.LoadInput(Day9TestData))
	if part1 != expected1 {
		t.Fatalf("Day 9 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 9 Part 2 expected %d, got %d", expected2, part2)
	}
}
