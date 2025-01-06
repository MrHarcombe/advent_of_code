package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
	"advent_of_code/2024.go/util"
	"fmt"
	"time"
)

type DataLoader struct {
	loadInput util.GetRawData
}

func makeLoader(grd util.GetRawData) *DataLoader {
	return &DataLoader{loadInput: grd}
}

func displayAnswers(part1, part2 int) {
	fmt.Println("Part 1:", part1)
	fmt.Println("Part 2:", part2)
}

func main() {
	var loader = makeLoader(util.LoadInput)

	begin := time.Now().UnixMilli()
	displayAnswers(day1.Solution(loader.loadInput("../2024/input1.txt")))
	displayAnswers(day2.Solution(loader.loadInput("../2024/input2.txt")))
	displayAnswers(day3.Solution(loader.loadInput("../2024/input3.txt")))
	displayAnswers(day4.Solution(loader.loadInput("../2024/input4.txt")))
	displayAnswers(day5.Solution(loader.loadInput("../2024/input5.txt")))
	fmt.Printf("Elapsed: %dms\n", time.Now().UnixMilli()-begin)
}
