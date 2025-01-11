package day7_test

import (
	"advent_of_code/2024.go/day7"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day7TestData = `190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`

func TestDay7(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 3749
	const expected2 = 11387

	var part1, part2 = day7.Solution(loader.LoadInput(Day7TestData))
	if part1 != expected1 {
		t.Fatalf("Day 7 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 7 Part 2 expected %d, got %d", expected2, part2)
	}
}
