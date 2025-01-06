package day5

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
)

func checkOrderings(page int, subPages []int, orderings map[int][]int) bool {
	if len(subPages) == 0 {
		return true
	}

	var isValid = true
	for _, after := range subPages {
		if !slices.Contains(orderings[page], after) {
			isValid = false
			break
		}
	}
	return isValid && checkOrderings(subPages[0], subPages[1:], orderings)
}

func correctOrderings(pages []int, orderings map[int][]int) []int {
	var correct = []int{pages[0]}
	for _, page := range pages[1:] {
		if len(orderings[page]) > 0 {
			var inserted = false
			for pos, corrected := range correct {
				if slices.Contains(orderings[page], corrected) {
					correct = slices.Insert(correct, pos, page)
					inserted = true
					break
				}
			}
			if !inserted {
				correct = append(correct, page)
			}
		} else {
			correct = append(correct, page)
		}
	}
	return correct
}

func Solution(rawData []string) {
	fmt.Println("2024 Day 5")
	// fmt.Println(rawData)

	var orderings = make(map[int][]int)
	var page int
	for ; len(rawData[page]) > 0; page++ {
		values := strings.Split(rawData[page], "|")
		v1, _ := strconv.Atoi(values[0])
		v2, _ := strconv.Atoi(values[1])
		orderings[v1] = append(orderings[v1], v2)
	}
	// fmt.Println(orderings)

	var updates [][]int
	for page++; page < len(rawData) && len(rawData[page]) > 0; page++ {
		values := strings.Split(rawData[page], ",")
		var pages []int
		for _, value := range values {
			v, _ := strconv.Atoi(value)
			pages = append(pages, v)
		}
		updates = append(updates, pages)
	}

	// fmt.Println(updates)
	var validMedians, invalidMedians int
	for _, update := range updates {
		if checkOrderings(update[0], update[1:], orderings) {
			validMedians += update[len(update)>>1]
		} else {
			update = correctOrderings(update, orderings)
			invalidMedians += update[len(update)>>1]
		}
	}

	fmt.Println("Part 1:", validMedians)
	fmt.Println("Part 2:", invalidMedians)
}
