package main

import (
	"fmt"
	"strconv"
)

func day_one(file_path string) {
	lines, err := read_file_to_array(file_path)
	if err != nil {
		fmt.Println(err)
	}
	max_calories := 0
	max_calorie_elf := 1
	current_calories := 0
	current_elf := 1

	for _, line := range lines {
		if line == "" {
			if current_calories > max_calories {
				max_calories = current_calories
				max_calorie_elf = current_elf
			}
			current_calories = 0
			current_elf += 1
		} else {
			calorie, _ := strconv.Atoi(line)
			current_calories += calorie
		}
	}
	fmt.Println("Elf", max_calorie_elf, "has the most calories:", max_calories)

}
