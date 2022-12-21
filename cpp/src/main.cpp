#include <map>
#include <iostream>
#include "static/aoc.h"


int main() {
    std::string file_path = "../../data/day_";
    std::map<int, std::string> file_paths;
    for (int i = 1; i <= 26; i++) {
        file_paths[i] = file_path + std::to_string(i);
    }
    AdventOfCode aoc;
    aoc.day_one(file_paths[1]);
    return 0;
}