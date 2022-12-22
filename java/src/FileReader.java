import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class FileReader {
    public static String[] read(String file_path)
        throws IOException
    {
        List<String> lines = new ArrayList<String>();
        lines = Files.readAllLines(Paths.get(file_path));
        String[] lines_array = lines.toArray(new String[lines.size()]);
        return lines_array;
    }
}
