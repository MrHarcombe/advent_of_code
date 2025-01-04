package main

import (
	"advent_of_code/2024.go/day1"
	"advent_of_code/2024.go/day2"
	"advent_of_code/2024.go/day3"
	"advent_of_code/2024.go/day4"
	"advent_of_code/2024.go/day5"
	"fmt"
	"os"
	"time"
)

func main() {
	if len(os.Args) > 1 && os.Args[1] == "test" {
		// day1.Solution("")
		// day2.Solution("")
		// day3.Solution("")
		// day4.Solution("")
		day5.Solution("")
	} else {
		begin := time.Now().UnixMilli()
		day1.Solution("../2024/input1.txt")
		day2.Solution("../2024/input2.txt")
		day3.Solution("../2024/input3.txt")
		day4.Solution("../2024/input4.txt")
		day5.Solution("../2024/input5.txt")
		fmt.Printf("Elapsed: %dms\n", time.Now().UnixMilli()-begin)
	}
}
