package day3

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

var memory string

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 3")

	var b strings.Builder
	for _, value := range rawData {
		fmt.Fprintf(&b, "%s", value)
	}
	memory = b.String()
	// fmt.Println(memory)

	var results1 int

	part1, _ := regexp.Compile(`mul\(([0-9]+),([0-9]+)\)`)
	matches1 := part1.FindAllStringSubmatch(memory, -1)
	for _, match1 := range matches1 {
		// fmt.Println(match1)
		m1, _ := strconv.Atoi(match1[1])
		m2, _ := strconv.Atoi(match1[2])
		results1 += m1 * m2
	}

	part2, _ := regexp.Compile(`(?:mul\(([0-9]+),([0-9]+)\))|(?:don\'t\(\))|(?:do\(\))`)
	matches2 := part2.FindAllStringSubmatch(memory, -1)
	results2 := 0
	includeInResults := true
	for _, match2 := range matches2 {
		// fmt.Println(match2)
		if strings.HasPrefix(match2[0], "m") && includeInResults {
			m1, _ := strconv.Atoi(match2[1])
			m2, _ := strconv.Atoi(match2[2])
			results2 += m1 * m2
		} else if strings.HasPrefix(match2[0], "don't") {
			includeInResults = false
		} else if strings.HasPrefix(match2[0], "do") {
			includeInResults = true
		}
	}

	return results1, results2
}
