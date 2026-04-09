/**
 * Represents a participant in the Tic Tac Toe game.
 * This abstract class is extended by concrete player types.
 */
public abstract class Player {
    protected final char symbol;
    protected final String name;

    /**
     * Creates a player with a display name and board symbol.
     *
     * @param name Display name for the player
     * @param symbol Symbol used on the board
     */
    public Player(String name, char symbol) {
        this.name = name;
        this.symbol = symbol;
    }

    /**
     * Gets the player's symbol.
     *
     * @return The character symbol used by the player
     */
    public char getSymbol() {
        return symbol;
    }

    /**
     * Gets the player's display name.
     *
     * @return The player name
     */
    public String getName() {
        return name;
    }

    /**
     * Calculates the player's next move based on game state.
     *
     * @param board Current board as a 9-cell array
     * @return Zero-based board index from 0 to 8
     */
    public abstract int getMove(char[] board);
}
