use std::{env, fs, io};
use std::io::BufReader;
use std::io::BufRead;
use std::collections::HashMap;
use std::hash::Hash;

pub fn day_one(file_path: String) -> io::Result<()> {
    let contents = file_to_vec(file_path);
    let calories_per_elf = iterate_elfs_group_calories(contents);
    let (max_calories_elf, max_calories) = get_max_calorie_elf(calories_per_elf).ok().unwrap();
    println!("Max calories: {} by elf: {}", max_calories, max_calories_elf);
    Ok(())
}


fn file_to_vec(file_path: String) -> io::Result<Vec<String>> {
    let file_in = fs::File::open(file_path)?;
    let file_reader = BufReader::new(file_in);
    Ok(file_reader.lines().filter_map(io::Result::ok).collect())
}

fn iterate_elfs_group_calories(calories: io::Result<Vec<String>>) -> io::Result<HashMap<i16, i32>> {
    let mut calories_per_elf: HashMap<i16, i32> = HashMap::new();
    calories_per_elf.insert(1, 0);
    let mut elf_id: i16 = 1;
    for value in calories.ok().unwrap() {
        if value.is_empty() {
            elf_id += 1;
            calories_per_elf.insert(elf_id, 0);
        } else {
            calories_per_elf.insert(elf_id, *calories_per_elf.get(&elf_id).unwrap() + value.parse::<i32>().unwrap());
        }
    }
    Ok(calories_per_elf)
}

fn get_max_calorie_elf(sum_calories_per_elf: io::Result<HashMap<i16, i32>>) -> io::Result<((i16, i32))> {
    let mut max_calorie_elf: i16 = 0;
    let mut max_calorie: i32 = 0;
    for (elf, calorie) in &sum_calories_per_elf.ok().unwrap() {
        if calorie > &max_calorie {
            max_calorie_elf = *elf;
            max_calorie = *calorie;
        }
    }
    Ok((max_calorie_elf, max_calorie))
}