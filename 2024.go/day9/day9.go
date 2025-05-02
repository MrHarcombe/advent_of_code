package day9

import (
	"advent_of_code/2024.go/util"
	"fmt"
	"slices"
	"strconv"
)

func makeDriveArray(data string) ([]int, map[int]int) {
	var driveArray []int
	var chunkMap = make(map[int]int)

	for offset, chunk := range data {
		chunkNumber := offset >> 1
		chunkSize, _ := strconv.Atoi(string(chunk))

		if offset%2 == 0 {
			driveArray = append(driveArray, slices.Repeat([]int{chunkNumber}, chunkSize)...)
			chunkMap[chunkNumber] = chunkSize
		} else {
			driveArray = append(driveArray, slices.Repeat([]int{-1}, chunkSize)...)
		}
	}
	return driveArray, chunkMap
}

func getDriveChecksum(driveArray []int) int {
	var checksum int
	for pos, chunk := range driveArray {
		if chunk != -1 {
			checksum += pos * chunk
		}
	}
	return checksum
}

func defrag_part1(driveArray []int) []int {
	for pos := len(driveArray) - 1; pos >= 0; pos-- {
		nextGap := slices.Index(driveArray, -1)
		if nextGap < pos {
			driveArray[nextGap] = driveArray[pos]
			driveArray[pos] = -1
		} else {
			break
		}
	}
	return driveArray
}

func defrag_part2(driveArray []int, chunkSize map[int]int) []int {
	sorted_chunks := make([]int, 0, len(chunkSize))
	for chunkNumber := range chunkSize {
		sorted_chunks = append(sorted_chunks, chunkNumber)
	}
	slices.SortFunc(sorted_chunks, func(a, b int) int {
		if a > b {
			return -1
		} else if a == b {
			return 0
		} else {
			return 1
		}
	})
	for _, chunk := range sorted_chunks {
		currentStart := slices.Index(driveArray, chunk)
		subSlice := slices.Repeat([]int{-1}, chunkSize[chunk])
		found := util.SearchSubSliceN[int](driveArray, subSlice, 1)
		if len(found) > 0 && found[0] < currentStart {
			for bit := 0; bit < chunkSize[chunk]; bit++ {
				driveArray[currentStart+bit] = -1
				driveArray[found[0]+bit] = chunk
			}
		}
	}
	return driveArray
}

func Solution(rawData []string) (int, int) {
	fmt.Println("2024 Day 9")

	var driveArray1, _ = makeDriveArray(rawData[0])
	driveArray1 = defrag_part1(driveArray1)
	var driveArray2, chunkMap2 = makeDriveArray(rawData[0])
	driveArray2 = defrag_part2(driveArray2, chunkMap2)

	return getDriveChecksum(driveArray1), getDriveChecksum(driveArray2)
}
