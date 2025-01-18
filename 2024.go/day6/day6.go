package day6

/*
 * worker pool solution adapted from
 * https://codelikemachine.com/8-go-performance-tips-i-discovered-after-years-of-coding/
 */

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

type warehouseJob struct {
	barrel    [2]int
	warehouse []string
	guard     guardDetails
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

func modelGuardMovement(grid []string, initial_guard guardDetails) bool {
	var visited = map[guardDetails]bool{initial_guard: true}
	for guard := takeStep(grid, initial_guard); string(grid[guard.row][guard.col]) != " "; guard = takeStep(grid, guard) {
		if visited[guard] {
			return true
		} else {
			visited[guard] = true
		}
	}
	return false
}

func modifyWarehouseThenModelGuard(barrel [2]int, grid []string, initialGuard guardDetails) bool {
	var new_grid = make([]string, len(grid))
	copy(new_grid, grid)
	new_grid[barrel[0]] = grid[barrel[0]][:barrel[1]] + string("#") + grid[barrel[0]][barrel[1]+1:]
	return modelGuardMovement(new_grid, initialGuard)
}

func workerPool(numWorkers int, jobs <-chan warehouseJob, results chan<- bool) {
	for i := 0; i < numWorkers; i++ {
		go worker(jobs, results)
	}
}

func worker(jobs <-chan warehouseJob, results chan<- bool) {
	for job := range jobs {
		results <- modifyWarehouseThenModelGuard(job.barrel, job.warehouse, job.guard)
	}
}

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 6")
	// fmt.Println(rawData)

	var grid = make([]string, len(rawData)+2)
	grid[0] = strings.Repeat(" ", len(rawData[0])+2)
	grid[len(grid)-1] = strings.Repeat(" ", len(rawData[0])+2)

	var initialGuard guardDetails
	for row, line := range rawData {
		if strings.ContainsAny(line, "^>v<") {
			for col, cell := range line {
				if string(cell) != "." && string(cell) != "#" {
					initialGuard = guardDetails{direction: directions_map[string(cell)], row: row + 1, col: col + 1}
					grid[row+1] = " " + rawData[row][:col] + "." + rawData[row][col+1:] + " "
					break
				}
			}
		} else {
			grid[row+1] = " " + line + " "
		}
	}
	// fmt.Println(guard, grid)

	var visited = map[[2]int]bool{[...]int{initialGuard.row, initialGuard.col}: true}
	for guard := takeStep(grid, initialGuard); string(grid[guard.row][guard.col]) != " "; guard = takeStep(grid, guard) {
		var coords = [...]int{guard.row, guard.col}
		visited[coords] = true
	}

	jobs := make(chan warehouseJob, len(visited))
	results := make(chan bool, len(visited))

	workerPool(500, jobs, results)

	for barrel := range visited {
		jobs <- warehouseJob{barrel: barrel, warehouse: grid, guard: initialGuard}
	}
	close(jobs)

	var loopings int
	for range visited {
		if <-results {
			loopings++
		}
	}

	return len(visited), loopings
}
