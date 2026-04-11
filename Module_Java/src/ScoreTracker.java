import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.TreeMap;

/**
 * Loads and saves scoreboard totals to a text file so results persist across runs.
 */
public class ScoreTracker {
    private final Path scoreFilePath;
    private final Map<String, Integer> winsByInitials;
    private int draws;

    /**
     * Creates a score tracker for a given file location.
     *
     * @param filePath Path to score data file
     */
    public ScoreTracker(String filePath) {
        this.scoreFilePath = Paths.get(filePath);
        this.winsByInitials = new TreeMap<>();
    }

    /**
     * Loads score values from disk if the file exists.
     */
    public void loadScores() {
        winsByInitials.clear();
        draws = 0;

        if (!Files.exists(scoreFilePath)) {
            return;
        }

        try (BufferedReader reader = Files.newBufferedReader(scoreFilePath)) {
            String line;
            while ((line = reader.readLine()) != null) {
                parseScoreLine(line);
            }
        } catch (IOException | NumberFormatException ex) {
            System.out.println("Could not read scores. Starting at 0. Reason: " + ex.getMessage());
            winsByInitials.clear();
            draws = 0;
        }
    }

    /**
     * Saves current score values to disk.
     */
    public void saveScores() {
        try {
            Path parent = scoreFilePath.getParent();
            if (parent != null && !Files.exists(parent)) {
                Files.createDirectories(parent);
            }

            try (BufferedWriter writer = Files.newBufferedWriter(scoreFilePath)) {
                writer.write("draws=" + draws);
                writer.newLine();

                for (Map.Entry<String, Integer> entry : winsByInitials.entrySet()) {
                    writer.write(entry.getKey() + "=" + entry.getValue());
                    writer.newLine();
                }
            }
        } catch (IOException ex) {
            System.out.println("Could not save scores. Reason: " + ex.getMessage());
        }
    }

    /**
     * Increases the win count for the supplied initials by one.
     *
     * @param initials Three-letter player initials
     */
    public void incrementWins(String initials) {
        String normalizedInitials = normalizeInitials(initials);
        int currentWins = winsByInitials.getOrDefault(normalizedInitials, 0);
        winsByInitials.put(normalizedInitials, currentWins + 1);
    }

    /**
     * Increases the draw count by one.
     */
    public void incrementDraws() {
        draws++;
    }

    /**
     * Gets the win total for the supplied initials.
     *
     * @param initials Three-letter player initials
     * @return Number of wins for these initials
     */
    public int getWins(String initials) {
        String normalizedInitials = normalizeInitials(initials);
        return winsByInitials.getOrDefault(normalizedInitials, 0);
    }

    /**
     * Gets draw total.
     *
     * @return Draws
     */
    public int getDraws() {
        return draws;
    }

    /**
     * Returns a copy of the current wins scoreboard sorted by initials.
     *
     * @return Copy of scoreboard wins map
     */
    public Map<String, Integer> getScoreboardWins() {
        return new TreeMap<>(winsByInitials);
    }

    /**
     * Parses a single key=value score line.
     *
     * @param line Input line from score file
     */
    private void parseScoreLine(String line) {
        line = line.trim();
        if (line.isEmpty()) {
            return;
        }

        String[] parts = line.split("=", 2);
        if (parts.length != 2) {
            return;
        }

        String key = parts[0].trim();
        int value = Integer.parseInt(parts[1].trim());

        if ("draws".equalsIgnoreCase(key)) {
            draws = value;
            return;
        }

        String normalizedInitials = normalizeInitials(key);
        winsByInitials.put(normalizedInitials, value);
    }

    /**
     * Normalizes initials to uppercase and 3 characters.
     *
     * @param initials Raw initials input
     * @return Normalized initials
     */
    private String normalizeInitials(String initials) {
        if (initials == null || initials.trim().isEmpty()) {
            return "UNK";
        }

        String cleaned = initials.trim().toUpperCase();
        if (cleaned.length() >= 3) {
            return cleaned.substring(0, 3);
        }

        return String.format("%-3s", cleaned).replace(' ', 'X');
    }
}
