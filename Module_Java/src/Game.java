import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/**
 * Coordinates menu flow, rounds, game logic, and score persistence.
 */
public class Game {
    private final Scanner scanner;
    private final ScoreTracker scoreTracker;
    private final List<String> gameHistory;
    private final String computerInitials;
    private String humanInitials;

    /**
     * Creates the game controller.
     */
    public Game() {
        this.scanner = new Scanner(System.in);
        this.scoreTracker = new ScoreTracker("data/scores.txt");
        this.gameHistory = new ArrayList<>();
        this.computerInitials = "CPU";
    }

    /**
     * Starts the game loop and handles the main menu.
     */
    public void run() {
        scoreTracker.loadScores();
        System.out.println("Welcome to Java Tic Tac Toe!");
        humanInitials = askInitials();

        boolean keepRunning = true;
        while (keepRunning) {
            printMenu();
            String option = scanner.nextLine().trim();

            switch (option) {
                case "1":
                    playRound();
                    break;
                case "2":
                    printScores();
                    break;
                case "3":
                    printHistory();
                    break;
                case "4":
                    keepRunning = false;
                    break;
                default:
                    System.out.println("Please choose 1, 2, 3, or 4.");
                    break;
            }
        }

        scoreTracker.saveScores();
        System.out.println("Scores saved. Thanks for playing!");
    }

    /**
     * Displays the menu options.
     */
    private void printMenu() {
        System.out.println();
        System.out.println("Menu");
        System.out.println("1) Play Round");
        System.out.println("2) View Scoreboard");
        System.out.println("3) View Session History");
        System.out.println("4) Quit");
        System.out.print("Select option: ");
    }

    /**
     * Runs one complete Tic Tac Toe round.
     */
    private void playRound() {
        char[] board = new char[9];
        initializeBoard(board);

        String difficulty = askDifficulty();
        Player human = new HumanPlayer(humanInitials, 'X', scanner);
        Player computer = new ComputerPlayer(computerInitials, 'O', difficulty);
        Player current = human;

        while (true) {
            printBoard(board);
            System.out.println(current.getName() + " turn (" + current.getSymbol() + ")");

            int move = current.getMove(board);
            board[move] = current.getSymbol();

            if (checkWin(board, current.getSymbol())) {
                printBoard(board);
                handleWin(current, difficulty);
                break;
            }

            if (checkDraw(board)) {
                printBoard(board);
                handleDraw(difficulty);
                break;
            }

            current = current == human ? computer : human;
        }
    }

    /**
     * Prompts for exactly three letters to identify the human player.
     *
     * @return Uppercase 3-letter initials
     */
    private String askInitials() {
        while (true) {
            System.out.print("Enter your 3-letter initials: ");
            String input = scanner.nextLine().trim().toUpperCase();
            if (input.matches("[A-Z]{3}")) {
                return input;
            }
            System.out.println("Please enter exactly 3 letters (A-Z). Example: PAK");
        }
    }

    /**
     * Initializes all board cells as empty spaces.
     *
     * @param board Board array to initialize
     */
    private void initializeBoard(char[] board) {
        for (int i = 0; i < board.length; i++) {
            board[i] = ' ';
        }
    }

    /**
     * Asks user to choose computer difficulty.
     *
     * @return "random" or "smart"
     */
    private String askDifficulty() {
        while (true) {
            System.out.print("Choose difficulty (1 = Random, 2 = Smart): ");
            String option = scanner.nextLine().trim();
            if ("1".equals(option)) {
                return "random";
            }
            if ("2".equals(option)) {
                return "smart";
            }
            System.out.println("Invalid option. Enter 1 or 2.");
        }
    }

    /**
     * Updates scores and history when someone wins.
     *
     * @param winner The player who won
     * @param difficulty Difficulty used in this round
     */
    private void handleWin(Player winner, String difficulty) {
        System.out.println(winner.getName() + " wins!");
        scoreTracker.incrementWins(winner.getName());

        String historyLine = String.format(
            "Result: %s won | Difficulty: %s | Totals %s",
            winner.getName(),
            difficulty,
            formatTotals()
        );
        gameHistory.add(historyLine);
        scoreTracker.saveScores();
    }

    /**
     * Updates scores and history when round ends in a draw.
     *
     * @param difficulty Difficulty used in this round
     */
    private void handleDraw(String difficulty) {
        System.out.println("Draw!");
        scoreTracker.incrementDraws();

        String historyLine = String.format(
            "Result: Draw | Difficulty: %s | Totals %s",
            difficulty,
            formatTotals()
        );
        gameHistory.add(historyLine);
        scoreTracker.saveScores();
    }

    /**
     * Builds a compact totals summary for history lines.
     *
     * @return Formatted totals string
     */
    private String formatTotals() {
        return String.format(
            "%s:%d %s:%d D:%d",
            humanInitials,
            scoreTracker.getWins(humanInitials),
            computerInitials,
            scoreTracker.getWins(computerInitials),
            scoreTracker.getDraws()
        );
    }

    /**
     * Prints the current board with row separators.
     *
     * @param board Current board state
     */
    public void printBoard(char[] board) {
        for (int row = 0; row < 3; row++) {
            int base = row * 3;
            System.out.println(
                " " + displayCell(board, base) + " | "
                + displayCell(board, base + 1) + " | "
                + displayCell(board, base + 2)
            );
            if (row < 2) {
                System.out.println("---+---+---");
            }
        }
        System.out.println();
    }

    /**
     * Displays either board symbol or position number for an empty cell.
     *
     * @param board Current board state
     * @param index Cell index to display
     * @return Cell display string
     */
    private String displayCell(char[] board, int index) {
        return board[index] == ' ' ? String.valueOf(index + 1) : String.valueOf(board[index]);
    }

    /**
     * Checks whether the given symbol has any winning line.
     *
     * @param board Current board state
     * @param symbol Symbol to evaluate
     * @return True if symbol has a winning line
     */
    public static boolean checkWin(char[] board, char symbol) {
        int[][] lines = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
            {0, 4, 8}, {2, 4, 6}
        };

        for (int[] line : lines) {
            if (board[line[0]] == symbol && board[line[1]] == symbol && board[line[2]] == symbol) {
                return true;
            }
        }
        return false;
    }

    /**
     * Checks whether the board is full with no winner.
     *
     * @param board Current board state
     * @return True when there are no empty cells
     */
    public static boolean checkDraw(char[] board) {
        for (char cell : board) {
            if (cell == ' ') {
                return false;
            }
        }
        return true;
    }

    /**
     * Prints currently stored scoreboard totals.
     */
    private void printScores() {
        System.out.println();
        System.out.println("Scoreboard");

        Map<String, Integer> wins = scoreTracker.getScoreboardWins();
        if (wins.isEmpty()) {
            System.out.println("No wins recorded yet.");
        } else {
            for (Map.Entry<String, Integer> entry : wins.entrySet()) {
                System.out.println(entry.getKey() + " Wins: " + entry.getValue());
            }
        }

        System.out.println("Draws: " + scoreTracker.getDraws());
    }

    /**
     * Prints all round results from this session.
     */
    private void printHistory() {
        System.out.println();
        System.out.println("Session History");
        if (gameHistory.isEmpty()) {
            System.out.println("No rounds played yet this session.");
            return;
        }

        for (int i = 0; i < gameHistory.size(); i++) {
            System.out.println((i + 1) + ". " + gameHistory.get(i));
        }
    }
}
