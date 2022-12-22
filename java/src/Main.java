import java.util.HashMap;

class AdventOfCode {

    public static void main(String[] args) {
        String base_path = "data/day_";
        HashMap<Integer, String> days = new HashMap<Integer, String>();

        for (int i = 1; i < 26; i++) {
            days.put(i, base_path + i);
        };
    

        DayOne.run(days.get(1));
    }
}
