package day4

import (
	"cmp"
	"fmt"
	"strings"
)

var rawData []string

func checkGridSlice(grid []string, row, col, rowEnd, dRow, dCol int, comparison string) bool {
	var b strings.Builder
	for r, c := row, col; r < rowEnd; r, c = r+dRow, c+dCol {
		fmt.Fprintf(&b, "%s", string(grid[r][c]))
	}
	possible := b.String()
	return cmp.Compare(possible, comparison) == 0
}

func countWordsOutFrom(grid []string, row, col int) int {
	var wordsOut int

	// Horizontal checks...
	if col > 2 && cmp.Compare(grid[row][col-3:col+1], "SAMX") == 0 {
		// fmt.Println(row, col, "Leftward match:", grid[row][col-3:col+1])
		wordsOut++
	}
	if col < len(grid[row])-3 && cmp.Compare(grid[row][col:col+4], "XMAS") == 0 {
		// fmt.Println(row, col, "Rightward match:", grid[row][col:col+4])
		wordsOut++
	}
	if row > 2 {
		// Check vertically upwards
		if checkGridSlice(grid, row-3, col, row+1, 1, 0, "SAMX") {
			wordsOut++
		}
		// Check diagonally right upwards
		if col > 2 {
			if checkGridSlice(grid, row-3, col-3, row+1, 1, 1, "SAMX") {
				wordsOut++
			}
		}
		// Check diagonally left upwards
		if col < len(grid[row])-3 {
			if checkGridSlice(grid, row-3, col+3, row+1, 1, -1, "SAMX") {
				wordsOut++
			}
		}
	}
	if row < len(grid)-3 {
		// Check vertically downwards
		if checkGridSlice(grid, row, col, row+4, 1, 0, "XMAS") {
			wordsOut++
		}
		// Check diagonally right downwards
		if col > 2 {
			if checkGridSlice(grid, row, col, row+4, 1, -1, "XMAS") {
				wordsOut++
			}
		}
		// Check diagonally left downwards
		if col < len(grid[row])-3 {
			if checkGridSlice(grid, row, col, row+4, 1, 1, "XMAS") {
				wordsOut++
			}
		}
	}

	return wordsOut
}

func countMSOutFrom(grid []string, row, col int) bool {
	var corners = [][]int{
		{-1, -1},
		{1, -1},
		{1, 1},
		{-1, 1}}
	var b strings.Builder
	for _, corner := range corners {
		r := corner[0]
		c := corner[1]
		fmt.Fprintf(&b, "%s", string(grid[row+r][col+c]))
	}
	possible := b.String()
	// fmt.Println(possible)
	return cmp.Compare(possible, "MSSM") == 0 || cmp.Compare(possible, "MMSS") == 0 || cmp.Compare(possible, "SMMS") == 0 || cmp.Compare(possible, "SSMM") == 0
}

func Solution(rawData []string) {
	fmt.Println("2024 Day 4")

	var grid = rawData
	// fmt.Println(grid)

	var foundXmas1, foundXmas2 int

	for r, row := range grid {
		for c, col := range row {
			if cmp.Compare(string(col), "X") == 0 {
				foundXmas1 += countWordsOutFrom(grid, r, c)
			}
			if r > 0 && r < len(grid)-1 && c > 0 && c < len(grid[r])-1 {
				if cmp.Compare(string(grid[r][c]), "A") == 0 && countMSOutFrom(grid, r, c) {
					foundXmas2++
				}
			}
		}
	}

	fmt.Println("Part 1:", foundXmas1)
	fmt.Println("Part 2:", foundXmas2)
}
