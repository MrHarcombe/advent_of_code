package day2

import (
	"bufio"
	"cmp"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

var test = []string{
	"7 6 4 2 1",
	"1 2 7 8 9",
	"9 7 6 2 1",
	"1 3 2 4 5",
	"8 6 4 4 1",
	"1 3 6 7 9"}

var reports [][]int

func Solution(fileName string) {
	fmt.Println("2024 Day 2")

	if len(fileName) == 0 || fileName == "test" {
		for _, value := range test {
			values := strings.Split(value, " ")
			var readings []int
			for _, value := range values {
				v, _ := strconv.Atoi(value)
				readings = append(readings, v)
			}
			reports = append(reports, readings)
		}
	} else {
		handle, error := os.Open(fileName)
		if error != nil {
			fmt.Println(error)
		}
		scanner := bufio.NewScanner(handle)
		scanner.Split(bufio.ScanLines)

		for scanner.Scan() {
			values := strings.Split(scanner.Text(), " ")
			var readings []int
			for _, value := range values {
				v, _ := strconv.Atoi(value)
				readings = append(readings, v)
			}
			reports = append(reports, readings)
		}
	}

	var unsafe int

	for _, report := range reports {
		var increasing = slices.IsSortedFunc(report, func(a, b int) int { return cmp.Compare(a, b) })
		var decreasing = slices.IsSortedFunc(report, func(a, b int) int { return -cmp.Compare(a, b) })
		if increasing || decreasing {
			previous := report[0]
			for _, value := range report[1:] {
				if previous == value || previous-value > 3 || value-previous > 3 {
					// fmt.Println("Unsafe:", previous, value)
					unsafe++
					break
				}
				previous = value
			}
		} else {
			// fmt.Println("Unsafe:", report)
			unsafe++
		}
	}

	fmt.Println("Part 1:", len(reports)-unsafe)
}
