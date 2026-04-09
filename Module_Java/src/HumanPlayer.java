import java.util.Scanner;

/**
 * Human-controlled player implementation.
 */
public class HumanPlayer extends Player {
    private final Scanner scanner;

    /**
     * Creates a human player.
     *
     * @param name Display name for the human player
     * @param symbol Board symbol used by the human player
     * @param scanner Shared scanner for reading console input
     */
    public HumanPlayer(String name, char symbol, Scanner scanner) {
        super(name, symbol);
        this.scanner = scanner;
    }

    /**
     * Prompts the user for a valid move and returns the selected index.
     *
     * @param board Current board state
     * @return Zero-based index for the human move
     */
    @Override
    public int getMove(char[] board) {
        while (true) {
            System.out.print("Choose a position (1-9): ");
            String input = scanner.nextLine().trim();

            if (!input.matches("[1-9]")) {
                System.out.println("Invalid input. Enter a number from 1 to 9.");
                continue;
            }

            int move = Integer.parseInt(input) - 1;
            if (board[move] != ' ') {
                System.out.println("That position is already taken. Try another.");
                continue;
            }

            return move;
        }
    }
}
