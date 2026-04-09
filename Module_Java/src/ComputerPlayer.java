import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Computer-controlled player with selectable difficulty.
 */
public class ComputerPlayer extends Player {
    private final String difficulty;
    private final Random random;

    /**
     * Creates a computer player.
     *
     * @param name Display name for the computer
     * @param symbol Board symbol used by the computer
     * @param difficulty AI mode: random or smart
     */
    public ComputerPlayer(String name, char symbol, String difficulty) {
        super(name, symbol);
        this.difficulty = difficulty;
        this.random = new Random();
    }

    /**
     * Selects a move based on difficulty mode.
     *
     * @param board Current board state
     * @return Zero-based board index for the computer move
     */
    @Override
    public int getMove(char[] board) {
        if ("smart".equalsIgnoreCase(difficulty)) {
            int bestMove = findSmartMove(board);
            if (bestMove != -1) {
                return bestMove;
            }
        }
        return findRandomMove(board);
    }

    /**
     * Finds a move using simple strategy:
     * 1) win if possible, 2) block opponent, 3) center, 4) random.
     *
     * @param board Current board state
     * @return Zero-based move index or -1 if none found
     */
    private int findSmartMove(char[] board) {
        int winMove = findWinningMove(board, this.symbol);
        if (winMove != -1) {
            return winMove;
        }

        char opponent = this.symbol == 'X' ? 'O' : 'X';
        int blockMove = findWinningMove(board, opponent);
        if (blockMove != -1) {
            return blockMove;
        }

        if (board[4] == ' ') {
            return 4;
        }

        return -1;
    }

    /**
     * Finds an immediate winning move for a given symbol.
     *
     * @param board Current board state
     * @param targetSymbol Symbol to test for winning move
     * @return Move index if found, otherwise -1
     */
    private int findWinningMove(char[] board, char targetSymbol) {
        for (int i = 0; i < board.length; i++) {
            if (board[i] == ' ') {
                board[i] = targetSymbol;
                boolean wins = Game.checkWin(board, targetSymbol);
                board[i] = ' ';
                if (wins) {
                    return i;
                }
            }
        }
        return -1;
    }

    /**
     * Selects a random move from all currently available cells.
     *
     * @param board Current board state
     * @return Random available move index
     */
    private int findRandomMove(char[] board) {
        List<Integer> availableMoves = new ArrayList<>();
        for (int i = 0; i < board.length; i++) {
            if (board[i] == ' ') {
                availableMoves.add(i);
            }
        }
        return availableMoves.get(random.nextInt(availableMoves.size()));
    }
}
