
public class DayOne {

    public static void run(String file_path) {

        try {
            String[] lines = FileReader.read(file_path);
            
            int max_calories = 0;
            int current_calories = 0;
            int max_calories_elf = 1;
            int current_elf = 1;
            
            for (String line : lines) {
                if (line.equals("")) {
                    if (current_calories > max_calories) {
                        max_calories = current_calories;
                        max_calories_elf = current_elf;
                    }
                    current_calories = 0;
                    current_elf++;
                } else {
                    current_calories += Integer.parseInt(line);
                }
            }
            System.out.println("Elf " + max_calories_elf + " has the most calories: " + max_calories);
        } catch (Exception e) {
            System.out.println("Error reading file: " + e);
        }


    }
}