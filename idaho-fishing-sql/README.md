# Overview

I built an Idaho Fishing Catch Tracker desktop application to strengthen my practical SQL and database integration skills using Python. The software uses a relational SQLite database to store and manage fishing catch records by date, body of water, county, species, and fish size.

The app provides a simple desktop UI where users can insert, modify, delete, and retrieve catch data. It also supports date-based filtering so users can view catches and the total number of catches for a specific date range.

My purpose for writing this software was to practice building SQL commands in application code, submitting those commands to a relational database, and using query results in a real interface.

# Relational Database

This project uses SQLite as the relational database engine through Python's built-in `sqlite3` library.

The main table is `catches`:

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `catch_date` (TEXT, stored as `YYYY-MM-DD`)
- `water_body` (TEXT)
- `county` (TEXT)
- `species` (TEXT)
- `size_in` (REAL, required and positive)
- `notes` (TEXT)

The software demonstrates:

- Insert (`INSERT INTO catches ...`)
- Modify (`UPDATE catches SET ... WHERE id = ?`)
- Delete (`DELETE FROM catches WHERE id = ?`)
- Retrieve (`SELECT ... FROM catches ...`)
- Date range filtering (`WHERE date(catch_date) >= date(?) AND date(catch_date) <= date(?)`)

# Development Environment

Tools used:

- Visual Studio Code
- Python 3.x
- SQLite (via Python `sqlite3`)
- Tkinter (desktop UI)

Programming language and libraries:

- Python
- Standard library modules: `sqlite3`, `tkinter`, `dataclasses`, `pathlib`, `typing`

## Running the Project

1. Open a terminal in this project folder.
2. Run:

```bash
python main.py
```

The database file is created automatically at `db/fishing.db` on first run.

# Useful Websites

- [CSE 310 SQL Module Guide](https://byui-cse.github.io/cse310-ww-course/modules/sql_database/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

# Future Work

- Add data export to CSV for catch reports.
- Add dropdown lists for frequently used water bodies and species.
- Add basic analytics charts for seasonal and species trends.

# Time Log

| Date       | Description                                        | Hours |
|------------|----------------------------------------------------|-------|
| 2026-03-09 | Researched sqlite3 module, planned schema and app structure | 5 |
| 2026-03-10 | Built schema.sql, wrote database.py CRUD functions | 5 |
| 2026-03-11 | Built Tkinter UI, form layout, and catches table   | 5 |
| 2026-03-12 | Added date filtering and records feature           | 2 |
| 2026-03-13 | Debugging, testing, and code cleanup               | 2 |
| 2026-03-14 | README, documentation, and final review            | 2.5 |
| **Total**  |                                                    | **21.5** |

# Discussion of Learning Strategies

During this module I practiced the Pomodoro technique—working in focused 25-minute blocks followed by short breaks—to stay productive across longer coding sessions. When I ran into unfamiliar SQLite behavior (such as how `date()` handles string comparisons), I first consulted the official SQLite documentation and then experimented with small test queries before integrating the solution. I also used spaced repetition by reviewing SQL syntax flashcards between work sessions to reinforce the INSERT, UPDATE, DELETE, and SELECT patterns covered in this module.
