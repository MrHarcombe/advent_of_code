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
