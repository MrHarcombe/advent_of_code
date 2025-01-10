package day6

import (
	"fmt"
	"strings"
)

const (
	up    = iota
	right = iota
	down  = iota
	left  = iota
)

var directions = [...]int{up, right, down, left}
var directions_map = map[string]int{"^": up, ">": right, "v": down, "<": left}
var directions_delta = map[int][]int{up: {-1, 0}, right: {0, 1}, down: {1, 0}, left: {0, -1}}

type guardDetails struct {
	direction int
	row       int
	col       int
}

func takeStep(grid []string, guard guardDetails) guardDetails {
	delta := directions_delta[guard.direction]
	next_row := guard.row + delta[0]
	next_col := guard.col + delta[1]
	next_dir := guard.direction

	for string(grid[next_row][next_col]) == "#" {
		next_dir = (next_dir + 1) % len(directions)
		delta = directions_delta[next_dir]
		next_row = guard.row + delta[0]
		next_col = guard.col + delta[1]
	}

	return guardDetails{direction: next_dir, row: next_row, col: next_col}
}

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 6")
	// fmt.Println(rawData)

	var grid = make([]string, len(rawData)+2)
	grid[0] = strings.Repeat(" ", len(rawData[0])+2)
	grid[len(grid)-1] = strings.Repeat(" ", len(rawData[0])+2)

	var initial_guard guardDetails
	for row, line := range rawData {
		if strings.ContainsAny(line, "^>v<") {
			for col, cell := range line {
				if string(cell) != "." && string(cell) != "#" {
					initial_guard = guardDetails{direction: directions_map[string(cell)], row: row + 1, col: col + 1}
					grid[row+1] = " " + rawData[row][:col] + "." + rawData[row][col+1:] + " "
					break
				}
			}
		} else {
			grid[row+1] = " " + line + " "
		}
	}
	// fmt.Println(guard, grid)

	var visited = map[[2]int]bool{[...]int{initial_guard.row, initial_guard.col}: true}
	for guard := takeStep(grid, initial_guard); string(grid[guard.row][guard.col]) != " "; guard = takeStep(grid, guard) {
		var coords = [...]int{guard.row, guard.col}
		visited[coords] = true
	}

	var loopings int
	for barrel := range visited {
		var new_grid = make([]string, len(grid))
		copy(new_grid, grid)
		new_grid[barrel[0]] = grid[barrel[0]][:barrel[1]] + string("#") + grid[barrel[0]][barrel[1]+1:]
		var new_visited = map[guardDetails]bool{initial_guard: true}
		for guard := takeStep(new_grid, initial_guard); string(new_grid[guard.row][guard.col]) != " "; guard = takeStep(new_grid, guard) {
			if new_visited[guard] {
				loopings++
				break
			} else {
				new_visited[guard] = true
			}
		}
	}

	return len(visited), loopings
}
