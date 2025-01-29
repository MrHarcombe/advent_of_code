package util

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func Abs(value int) int {
	if value < 0 {
		return -value
	} else {
		return value
	}
}

func LoadLocalInput(test_data string) []string {
	var input_data []string

	for _, line := range strings.Split(test_data, "\n") {
		input_data = append(input_data, strings.TrimSpace(line))
	}

	return input_data
}

func LoadFileInput(file string) []string {
	var input_data []string

	handle, error := os.Open(file)
	if error != nil {
		fmt.Println(error)
	}
	scanner := bufio.NewScanner(handle)
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		input_data = append(input_data, scanner.Text())
	}

	return input_data
}

type GetRawData func(file string) []string

type DataLoader struct {
	LoadInput GetRawData
}

func MakeLoader(grd GetRawData) *DataLoader {
	return &DataLoader{LoadInput: grd}
}

func Enqueue(queue []int, value int) []int {
	queue = append(queue, value)
	return queue
}

func Dequeue(queue []int) ([]int, *int) {
	var value (*int)
	if len(queue) > 0 {
		value = &queue[0]
		queue = queue[1:]
	}
	return queue, value
}

func IsEmpty(queue []int) bool {
	return len(queue) == 0
}

/*
 * SearchSubSlice and SearchSubSliceN both adapted from
 * https://gist.github.com/MOOOWOOO/8c8668d3b336d80f4e42ee794a439012.js
 */

// search all sub slices
func SearchSubSlice[S comparable](mainSlice, subSlice []S) []int {
	var result []int
	result = nil

	// if main slice is nil or empty, just return nil
	if mainSlice == nil {
		return result
	}
	mainSliceLen := len(mainSlice)
	if mainSliceLen == 0 {
		return result
	}

	// if sub slice is nil or empty, just return nil
	if subSlice == nil {
		return result
	}
	subSliceLen := len(subSlice)
	if subSliceLen == 0 {
		return result
	}

	// if main slice is shorter than sub slice, just return nil
	if mainSliceLen < subSliceLen {
		return result
	}

	// index offset of first element of sub slice in main slice when sub slice is found in main slice
	indexOffset := subSliceLen - 1

	// sub slice seek
	subSliceSeek := 0
	// total match times check point, max value is length of sub slice which means match success
	checkPoint := 0

	// loop main slice
	for index, value := range mainSlice {
		if value == subSlice[subSliceSeek] {
			// once an element matches

			// sub slice seek move forward
			subSliceSeek++
			// check point ++
			checkPoint++

		} else {
			// once an element mismatches, reset sub slice seek & check point
			subSliceSeek = 0
			checkPoint = 0

			// after reset, retry to match first element of sub slice
			// in case of missed [a,b] [a,a,b]
			if value == subSlice[subSliceSeek] {
				subSliceSeek++
				checkPoint++
			}
		}

		// once all elements in sub slice matches, store the first element index into result slice.
		if checkPoint == subSliceLen {
			result = append(result, index-indexOffset)
			subSliceSeek = 0
			checkPoint = 0
		}
	}

	return result
}

// search first N times sub slices
func SearchSubSliceN[S comparable](mainSlice, subSlice []S, N int) []int {
	var result []int
	result = nil

	// if main slice is nil or empty, just return nil
	if mainSlice == nil {
		return result
	}
	mainSliceLen := len(mainSlice)
	if mainSliceLen == 0 {
		return result
	}

	// if sub slice is nil or empty, just return nil
	if subSlice == nil {
		return result
	}
	subSliceLen := len(subSlice)
	if subSliceLen == 0 {
		return result
	}

	// if main slice is shorter than sub slice, just return nil
	if mainSliceLen < subSliceLen {
		return result
	}

	// index offset of first element of sub slice in main slice when sub slice is found in main slice
	indexOffset := subSliceLen - 1

	// sub slice seek
	subSliceSeek := 0
	// total match times check point, max value is length of sub slice which means match success
	checkPoint := 0

	// result length
	resultLen := 0

	// loop main slice
	for index, value := range mainSlice {
		if value == subSlice[subSliceSeek] {
			// once an element matches

			// sub slice seek move forward
			subSliceSeek++
			// check point ++
			checkPoint++

		} else {
			// once an element mismatches, reset sub slice seek & check point
			subSliceSeek = 0
			checkPoint = 0

			// after reset, retry to match first element of sub slice
			// in case of missed [a,b] [a,a,b]
			if value == subSlice[subSliceSeek] {
				subSliceSeek++
				checkPoint++
			}
		}

		// once all elements in sub slice matches, store the first element index into result slice.
		if checkPoint == subSliceLen {
			result = append(result, index-indexOffset)
			resultLen++
			subSliceSeek = 0
			checkPoint = 0
		}

		// if result element is up to preset N times break the loop
		if N == resultLen {
			break
		}
	}

	return result
}
