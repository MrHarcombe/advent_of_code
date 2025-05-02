package day8

import (
	"fmt"

	"gonum.org/v1/gonum/stat/combin"
)

func checkSingleLocation(locations map[[2]int]bool, antenna [2]int, dx, dy int, width, height int) {
	if antenna[0]+dx >= 0 && antenna[0]+dx < width {
		if antenna[1]+dy >= 0 && antenna[1]+dy < height {
			locations[[...]int{antenna[0] + dx, antenna[1] + dy}] = true
		}
	}
}

func checkAllLocations(locations map[[2]int]bool, antenna [2]int, dx, dy int, width, height int) {
	var x = antenna[0]
	var y = antenna[1]
	for x+dx >= 0 && x+dx < width && y+dy >= 0 && y+dy < height {
		locations[[...]int{x + dx, y + dy}] = true
		x += dx
		y += dy
	}
}

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 8")

	var part1_locations = make(map[[2]int]bool)
	var part2_locations = make(map[[2]int]bool)

	var cityMap = make(map[string][][2]int)
	for row, line := range rawData {
		for col, ch := range line {
			if string(ch) != "." {
				cityMap[string(ch)] = append(cityMap[string(ch)], [2]int{row, col})
				part2_locations[[2]int{row, col}] = true
			}
		}
	}

	for antennae, locations := range cityMap {
		if len(locations) > 1 {
			var pairs = combin.Combinations(len(locations), 2)
			for _, pair := range pairs {
				// fmt.Println(antennae, "->", cityMap[antennae][pair[0]], cityMap[antennae][pair[1]])

				var dx = cityMap[antennae][pair[0]][0] - cityMap[antennae][pair[1]][0]
				var dy = cityMap[antennae][pair[0]][1] - cityMap[antennae][pair[1]][1]

				// fmt.Println(dx, dy)
				checkSingleLocation(part1_locations, cityMap[antennae][pair[0]], dx, dy, len(rawData[0]), len(rawData))
				checkSingleLocation(part1_locations, cityMap[antennae][pair[1]], -dx, -dy, len(rawData[0]), len(rawData))

				checkAllLocations(part2_locations, cityMap[antennae][pair[0]], dx, dy, len(rawData[0]), len(rawData))
				checkAllLocations(part2_locations, cityMap[antennae][pair[1]], -dx, -dy, len(rawData[0]), len(rawData))
			}
		}
	}

	return len(part1_locations), len(part2_locations)
}
