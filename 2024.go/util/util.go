package util

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type GetRawData func(file string) []string

func LoadInput(file string) []string {
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

func LoadTestInput(test_data string) []string {
	var input_data []string

	for _, line := range strings.Split(test_data, "\n") {
		input_data = append(input_data, strings.TrimSpace(line))
	}

	return input_data
}
