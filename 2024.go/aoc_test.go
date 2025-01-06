package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
	"advent_of_code/2024.go/day6"
	"advent_of_code/2024.go/test"
	"strings"
	"testing"
)

func LoadTestInput(test_data string) []string {
	var input_data []string

	for _, line := range strings.Split(test_data, "\n") {
		input_data = append(input_data, strings.TrimSpace(line))
	}

	return input_data
}

func TestDay1(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 11
	const expected2 = 31

	var part1, part2 = day1.Solution(loader.loadInput(test.Day1TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}

func TestDay2(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 2
	const expected2 = 4

	var part1, part2 = day2.Solution(loader.loadInput(test.Day2TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}

func TestDay3(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 161
	const expected2 = 48

	var part1, part2 = day3.Solution(loader.loadInput(test.Day3TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}

func TestDay4(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 18
	const expected2 = 9

	var part1, part2 = day4.Solution(loader.loadInput(test.Day4TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}

func TestDay5(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 143
	const expected2 = 123

	var part1, part2 = day5.Solution(loader.loadInput(test.Day5TestData))
	if part1 != expected1 {
		t.Fatalf("Day 1 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 1 Part 2 expected %d, got %d", expected2, part2)
	}
}

func TestDay6(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	const expected1 = 41
	const expected2 = 6

	var part1, part2 = day6.Solution(loader.loadInput(test.Day6TestData))
	if part1 != expected1 {
		t.Fatalf("Day 6 Part 1 expected %d, got %d", expected1, part1)
	}
	if part2 != expected2 {
		t.Fatalf("Day 6 Part 2 expected %d, got %d", expected2, part2)
	}
}
