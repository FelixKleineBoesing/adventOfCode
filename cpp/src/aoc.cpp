#include <iostream>
#include <fstream>
#include <string>
#include "static/aoc.h"

void AdventOfCode::day_one(const std::string& file_path)
{
    std::ifstream dataFile;
    dataFile.open(file_path, std::ios::in);
    if (!dataFile) {
        std::cout << "file does not exist" << std::endl;
    }
    int32_t max_calories = 0;
    int16_t max_calorie_elf = 1;
    int32_t current_calories = 0;
    int16_t current_elf = 1;


    if (dataFile.is_open()) {
        std::string line;
        while (std::getline(dataFile, line)) {
            if (line.empty()) {
                if (current_calories > max_calories) {
                    max_calories = current_calories;
                    max_calorie_elf = current_elf;
                }
                current_calories = 0;
                current_elf++;
            } else {
                current_calories += std::stoi(line);
            }
        }
    }
    dataFile.close();

    std::cout << "Elf " << max_calorie_elf << " has the most calories:" << max_calories << std::endl;
}

