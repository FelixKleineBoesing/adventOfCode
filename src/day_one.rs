use std::env;
use std::fs;

fn main(file_path: String) {

}

fn read_data(file_path: String) {
    println!("In file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}

fn iterate_elfs_group_calories() {

}