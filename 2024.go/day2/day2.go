package day2

import (
	"cmp"
	"fmt"
	"slices"
	"strconv"
	"strings"
)

var TestData = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

var reports [][]int

func checkReportIsSafe(report []int) bool {
	var increasing = slices.IsSortedFunc(report, func(a, b int) int { return cmp.Compare(a, b) })
	var decreasing = slices.IsSortedFunc(report, func(a, b int) int { return -cmp.Compare(a, b) })

	if !(increasing || decreasing) {
		return false
	}

	previous := report[0]
	for _, value := range report[1:] {
		if previous == value || previous-value > 3 || value-previous > 3 {
			return false
		}
		previous = value
	}
	return true
}

func Solution(rawData []string) {
	fmt.Println("2024 Day 2")

	for _, value := range rawData {
		values := strings.Split(value, " ")
		var readings []int
		for _, value := range values {
			v, _ := strconv.Atoi(value)
			readings = append(readings, v)
		}
		reports = append(reports, readings)
	}

	var safe_1 int
	var safe_2 int

	for _, report := range reports {
		if checkReportIsSafe(report) {
			safe_1++
			safe_2++
		} else {
			for i := range report {
				sub_report := slices.Concat(report[:i], report[i+1:])
				if checkReportIsSafe(sub_report) {
					safe_2++
					break
				}
			}
		}
	}

	fmt.Println("Part 1:", safe_1)
	fmt.Println("Part 2:", safe_2)
}
