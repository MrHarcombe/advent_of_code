package day2

import (
	"cmp"
	"fmt"
	"slices"
	"strconv"
	"strings"
)

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

func Solution(rawData []string) (int, int) {
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

	var safe1 int
	var safe2 int

	for _, report := range reports {
		if checkReportIsSafe(report) {
			safe1++
			safe2++
		} else {
			for i := range report {
				sub_report := slices.Concat(report[:i], report[i+1:])
				if checkReportIsSafe(sub_report) {
					safe2++
					break
				}
			}
		}
	}

	return safe1, safe2
}
