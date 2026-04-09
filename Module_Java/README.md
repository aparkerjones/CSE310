# Overview

I built this project to get better at writing Java that actually feels usable, not just classroom examples. My goal was to build something from scratch, keep it organized, and make sure I could explain every part of it.

This software is a console-based Tic Tac Toe game where a human player competes against a computer opponent. You can choose difficulty (Random or Smart), play multiple rounds, and check both score totals and session history from the menu.

I wrote this to practice core Java syntax in one project and to get more comfortable with inheritance and file I/O in a real workflow.

# Development Environment

Tools used:
- Visual Studio Code
- Java Development Kit (JDK)
- PowerShell terminal

Language and libraries:
- Java
- Java standard library packages: `java.util`, `java.io`, `java.nio.file`

## Running the Project

Prerequisites:
- Java JDK installed (OpenJDK 21+ recommended)
- `java` and `javac` available in PATH

From the `Module_Java` folder:

```bash
javac src/*.java
java -cp src Main
```

Scores are saved to:
- `data/scores.txt`

# Useful Websites

- [Oracle Java Documentation](https://docs.oracle.com/en/java/)
- [W3Schools Java Tutorial](https://www.w3schools.com/java/)
- [Java NIO File API Guide](https://docs.oracle.com/javase/tutorial/essential/io/file.html)
- [GeeksforGeeks Tic Tac Toe Logic Reference](https://www.geeksforgeeks.org/tic-tac-toe-game-in-java/)

# Future Work

- Add symbol selection so the user can choose X or O.
- Keep AI simple but add a few smarter opening moves.
- Export game history to a file for long-term analytics.
- Add unit tests for win checking and score file parsing.
- Package the project with a build tool like Gradle.

## Requirement Mapping

- Variables: board cells, symbols, initials, score counters, turn tracker
- Expressions: win-line evaluation, initials-based scoreboard totals, index calculations
- Conditionals: input checks, initials validation, move validation, winner/draw logic, menu routing
- Loops: main menu loop, round loop, input validation loops, score file read loop
- Functions: I split the game into focused methods such as `printBoard`, `checkWin`, `checkDraw`, `getMove`, `saveScores`, and `loadScores` plus initials helpers
- Classes: `Game`, `Player`, `HumanPlayer`, `ComputerPlayer`, `ScoreTracker`, `Main`
- Java collection framework: `ArrayList<String>` session history and `TreeMap<String, Integer>` initials-based wins
- Additional requirement implemented:
  - File read/write for persistent initials-based scores (`data/scores.txt`)
  - Inheritance with `abstract` + `extends` in `Player`, `HumanPlayer`, and `ComputerPlayer`

## Time Log (20+ Hours)

| Date       | Description | Hours |
|------------|-------------|-------|
| 2026-03-24 | Environment setup and Java refresher | 2.0 |
| 2026-03-25 | Practice with variables, conditionals, loops | 2.0 |
| 2026-03-26 | OOP planning and class design | 2.0 |
| 2026-03-27 | Build player inheritance model | 2.0 |
| 2026-03-28 | Core board and turn-taking game loop | 2.0 |
| 2026-03-31 | Win/draw detection and edge-case testing | 2.0 |
| 2026-04-01 | File save/load implementation for scores | 2.0 |
| 2026-04-02 | Add `ArrayList` round history and summary output | 2.0 |
| 2026-04-03 | Playtesting and input validation improvements | 2.0 |
| 2026-04-04 | Final cleanup, README, and rubric check | 2.0 |
| **Total**  |             | **20.0** |

## Project Notes

- I kept the AI intentionally simple so the code stays easy to explain.
- I focused most of my effort on clean game flow, input handling, and persistence.
- I tested after each small change so I did not end up with one huge debugging session.

## Discussion of Learning Strategies

I built this in small chunks and tested each chunk before moving on. That made bugs easier to isolate and gave me cleaner progress each day. For the parts I was less familiar with (especially file I/O), I did quick throwaway tests first and then moved the working version into the project.
