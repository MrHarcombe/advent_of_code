package util

import (
	"bufio"
	"fmt"
	"os"
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
