package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
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

	day1.Solution(loader.loadInput(test.Day1TestData))
}

func TestDay2(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	day2.Solution(loader.loadInput(test.Day2TestData))
}

func TestDay3(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	day3.Solution(loader.loadInput(test.Day3TestData))
}

func TestDay4(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	day4.Solution(loader.loadInput(test.Day4TestData))
}

func TestDay5(t *testing.T) {
	var loader = makeLoader(LoadTestInput)

	day5.Solution(loader.loadInput(test.Day5TestData))
}
