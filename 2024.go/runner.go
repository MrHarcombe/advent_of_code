package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"os"
)

func main() {
	if len(os.Args) > 1 && os.Args[1] == "test" {
		day1.Solution("test")
		day2.Solution("test")
	} else {
		day1.Solution("../2024/input1.txt")
		day2.Solution("../2024/input2.txt")
	}
}
