package main

import (
	"strconv"
)

func main() {

	base_path := "../../data/day_"
	var days = make(map[int]string)

	for i := 1; i <= 25; i++ {
		days[i] = base_path + strconv.Itoa(i)
	}
	day_one(days[1])

}
