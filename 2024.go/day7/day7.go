package day7

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func calculate_possibles(target int, initial_value int, operands []int, part2 bool) []int {
	var current_totals = []int{initial_value}

	for len(operands) > 0 {
		var next_value = operands[0]
		operands = operands[1:]

		var new_totals []int
		for _, running_total := range current_totals {
			if next_value+running_total <= target {
				new_totals = append(new_totals, next_value+running_total)
			}
			if next_value*running_total <= target {
				new_totals = append(new_totals, next_value*running_total)
			}
			if part2 {
				var digits = int(math.Ceil(math.Log10(float64(next_value)+0.1)))
				if running_total*int(math.Pow(10, float64(digits)))+next_value <= target {
					new_totals = append(new_totals, running_total*int(math.Pow(10, float64(digits)))+next_value)
				}
			}
		}
		current_totals = make([]int, len(new_totals))
		copy(current_totals, new_totals)
	}
	// fmt.Println(target, part2, current_totals)

	return current_totals
}

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 7")

	var calibrations [][]int
	for _, line := range rawData {
		parts := strings.Split(line, " ")
		value, _ := strconv.Atoi(strings.TrimSuffix(parts[0], ":"))
		calibration := []int{value}
		for _, operand := range parts[1:] {
			value, _ = strconv.Atoi(operand)
			calibration = append(calibration, value)
		}
		calibrations = append(calibrations, calibration)
	}
	// fmt.Println(calibrations)

	var found1, found2 int
	for _, calibration := range calibrations {
		var target = calibration[0]
		var initial = calibration[1]

		// trim those values off
		var operands1 = make([]int, len(calibration[2:]))
		copy(operands1, calibration[2:])

		var totals1 = calculate_possibles(target, initial, operands1, false)
		for _, value := range totals1 {
			if value == target {
				found1 += value
				break
			}
		}

		var operands2 = make([]int, len(calibration[2:]))
		copy(operands2, calibration[2:])

		var totals2 = calculate_possibles(target, initial, operands1, true)
		for _, value := range totals2 {
			if value == target {
				found2 += value
				break
			}
		}
	}

	return found1, found2
}
