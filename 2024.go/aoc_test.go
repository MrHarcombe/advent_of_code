package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
	"advent_of_code/2024.go/util"
	"testing"
)

func TestDay1(t *testing.T) {
	var loader = makeLoader(util.LoadTestInput)

	day1.Solution(loader.loadInput(day1.TestData))
}

func TestDay2(t *testing.T) {
	var loader = makeLoader(util.LoadTestInput)

	day2.Solution(loader.loadInput(day2.TestData))
}

func TestDay3(t *testing.T) {
	var loader = makeLoader(util.LoadTestInput)

	day3.Solution(loader.loadInput(day3.TestData))
}

func TestDay4(t *testing.T) {
	var loader = makeLoader(util.LoadTestInput)

	day4.Solution(loader.loadInput(day4.TestData))
}

func TestDay5(t *testing.T) {
	var loader = makeLoader(util.LoadTestInput)

	day5.Solution(loader.loadInput(day5.TestData))
}
