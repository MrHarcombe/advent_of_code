package day5_test

import (
	"advent_of_code/2024.go/day5"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day5TestData = `47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47`

func TestDay5(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 143
	const expected2 = 123

	var part1, part2 = day5.Solution(loader.LoadInput(Day5TestData))
	if part1 != expected1 {
		t.Fatalf("Day 5 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 5 Part 2 expected %d, got %d", expected2, part2)
	}
}
