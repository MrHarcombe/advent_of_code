package util

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func LoadInput(fileName string, test_data []string) []string {
	var input_data []string

	if len(fileName) == 0 || fileName == "test" {
		for _, line := range test_data {
			input_data = append(input_data, strings.TrimSpace(line))
		}
	} else {
		handle, error := os.Open(fileName)
		if error != nil {
			fmt.Println(error)
		}
		scanner := bufio.NewScanner(handle)
		scanner.Split(bufio.ScanLines)

		for scanner.Scan() {
			input_data = append(input_data, scanner.Text())
		}
	}

	return input_data
}
