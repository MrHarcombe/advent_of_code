package day5

import (
	"advent_of_code/2024.go/util"
	"fmt"
	"slices"
	"strconv"
	"strings"
)

var test = []string{"47|53",
	"97|13",
	"97|61",
	"97|47",
	"75|29",
	"61|13",
	"75|53",
	"29|13",
	"97|29",
	"53|29",
	"61|53",
	"97|53",
	"61|29",
	"47|13",
	"75|47",
	"97|75",
	"47|61",
	"75|61",
	"47|29",
	"75|13",
	"53|13",
	"",
	"75,47,61,53,29",
	"97,61,53,29,13",
	"75,29,13",
	"75,97,47,61,53",
	"61,13,29",
	"97,13,75,29,47"}

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

func Solution(fileName string) {
	fmt.Println("2024 Day 5")

	var input = util.LoadInput(fileName, test)
	// fmt.Println(input)

	var orderings = make(map[int][]int)

	var page int
	for ; len(input[page]) > 0; page++ {
		values := strings.Split(input[page], "|")
		v1, _ := strconv.Atoi(values[0])
		v2, _ := strconv.Atoi(values[1])
		orderings[v1] = append(orderings[v1], v2)
	}
	// fmt.Println(orderings)

	var updates [][]int
	for page++; page < len(input) && len(input[page]) > 0; page++ {
		values := strings.Split(input[page], ",")
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
