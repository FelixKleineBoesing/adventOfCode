mod day_one;
mod day_two;

use std::env;
use day_one::day_one;
use day_two::day_two;

fn main() {
    println!("Start Programm!");
    let args: Vec<String> = env::args().collect();
    println!("Args: {:?}", args);
    let day: &str = &args[1];

    if day == "1" {
        let file_path: String = "../data/day_1.txt".to_string();
        day_one(file_path);
    } else if day == "2" {
        let file_path: String = "../data/day_2.txt".to_string();
    }
}
