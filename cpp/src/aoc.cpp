#include <iostream>
#include <fstream>
#include <string>
#include "static/aoc.h"

void AdventOfCode::day_one(const std::string& file_path)
{
    std::ifstream dataFile;
    // check if file exists


    dataFile.open(file_path, std::ios::in);
    if (!dataFile) {
        std::cout << "file does not exist" << std::endl;
    }
    if (dataFile.is_open()) {
        std::string line;
        while (std::getline(dataFile, line)) {
            std::cout << line << std::endl;
        }
    }
    dataFile.close();
}