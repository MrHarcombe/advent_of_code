package day1

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

var left []int
var right []int

func count[T any](slice []T, f func(T) bool) int {
	var count int
	for _, s := range slice {
		if f(s) {
			count++
		}
	}
	return count
}

func Solution(rawData []string) {
	fmt.Println("2024 Day 1")

	for _, value := range rawData {
		values := strings.Split(value, "   ")
		v1, _ := strconv.Atoi(values[0])
		v2, _ := strconv.Atoi(values[1])
		left = append(left, v1)
		right = append(right, v2)
	}

	sort.Ints(left)
	sort.Ints(right)

	var distance int
	for i := range left {
		if left[i] > right[i] {
			distance += left[i] - right[i]
		} else {
			distance += right[i] - left[i]
		}
	}

	fmt.Println("Part 1:", distance)

	var similarity int
	for _, value := range left {
		similarity += value * count(right, func(m int) bool {
			return m == value
		})
	}

	fmt.Println("Part 2:", similarity)
}
