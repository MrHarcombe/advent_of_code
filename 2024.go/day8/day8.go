package day8

import (
	"fmt"

	"gonum.org/v1/gonum/stat/combin"
)

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 8")

	var cityMap = make(map[string][][2]int)
	for row, line := range rawData {
		for col, ch := range line {
			if string(ch) != "." {
				cityMap[string(ch)] = append(cityMap[string(ch)], [2]int{row, col})
			}
		}
	}

	for antennae, locations := range cityMap {
		if len(locations) > 1 {
			var pairs = combin.Combinations(len(locations), 2)
			for _, pair := range pairs {
				fmt.Println(antennae, "->", cityMap[antennae][pair[0]], cityMap[antennae][pair[1]])
			}
		}
	}

	return 0, 0
}
