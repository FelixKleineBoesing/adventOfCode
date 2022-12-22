const fs = require("fs");

const base_path = "../data/day_"
const file_paths = new Map();

for (let i = 1; i < 26; i ++) {
  file_paths.set(i, base_path + i)
}

'use strict';
function dayOne() {
  arr = syncReadFile(file_paths.get(1));
  console.log(arr);
  max_calories = 0;
  max_calories_elf = 1;
  current_calories = 0;
  current_elf = 1;
  for (let i = 0; i < arr.length(); i++) {
    if (arr[i] == "") {
      if (current_calories > max_calories) {
        max_calories = current_calories;
        max_calories_elf = current_elf;
      }
      current_elf ++;
      current_calories = 0;
    } else {
      current_calories += Number(arr[i])
    }
  }
  document.getElementById('dayOne').innerHTML = "The max calories are: " + max_calories + ", carried by the elf: " + max_calories_elf;
}
dayOne()

function syncReadFile(file_path)
{
    const contents = fs.readFileSync(file_path)
    const arr = contents.split(/\r?\n/);
    return arr
}