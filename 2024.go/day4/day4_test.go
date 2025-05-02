package day4_test

import (
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/util"
	"testing"
)

var Day4TestData = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`

func TestDay4(t *testing.T) {
	var loader = util.MakeLoader(util.LoadLocalInput)

	const expected1 = 18
	const expected2 = 9

	var part1, part2 = day4.Solution(loader.LoadInput(Day4TestData))
	if part1 != expected1 {
		t.Fatalf("Day 4 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 4 Part 2 expected %d, got %d", expected2, part2)
	}
}
