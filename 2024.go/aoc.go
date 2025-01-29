package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
	"advent_of_code/2024.go/day6"
	"advent_of_code/2024.go/day7"
	"advent_of_code/2024.go/day8"
	"advent_of_code/2024.go/day9"
	"advent_of_code/2024.go/util"
	"fmt"
	"time"
)

func displayAnswers(part1, part2 int) {
	fmt.Println("Part 1:", part1)
	fmt.Println("Part 2:", part2)
}

func main() {
	var loader = util.MakeLoader(util.LoadFileInput)

	begin := time.Now().UnixMilli()
	displayAnswers(day1.Solution(loader.LoadInput("../2024/input1.txt")))
	displayAnswers(day2.Solution(loader.LoadInput("../2024/input2.txt")))
	displayAnswers(day3.Solution(loader.LoadInput("../2024/input3.txt")))
	displayAnswers(day4.Solution(loader.LoadInput("../2024/input4.txt")))
	displayAnswers(day5.Solution(loader.LoadInput("../2024/input5.txt")))
	displayAnswers(day6.Solution(loader.LoadInput("../2024/input6.txt")))
	displayAnswers(day7.Solution(loader.LoadInput("../2024/input7.txt")))
	displayAnswers(day8.Solution(loader.LoadInput("../2024/input8.txt")))
	displayAnswers(day9.Solution(loader.LoadInput("../2024/input9.txt")))
	fmt.Printf("Elapsed: %dms\n", time.Now().UnixMilli()-begin)
}
