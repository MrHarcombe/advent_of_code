package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"fmt"
	"os"
	"time"
)

func main() {
	if len(os.Args) > 1 && os.Args[1] == "test" {
		day1.Solution("test")
		day2.Solution("test")
		day3.Solution("test")
		day4.Solution("test")
	} else {
		begin := time.Now().UnixMilli()
		day1.Solution("../2024/input1.txt")
		day2.Solution("../2024/input2.txt")
		day3.Solution("../2024/input3.txt")
		day4.Solution("../2024/input4.txt")
		fmt.Printf("Elapsed: %dms\n", time.Now().UnixMilli()-begin)
	}
}
