import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "fishing.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"


@dataclass
class CatchRecord:
    id: int
    catch_date: str
    water_body: str
    county: str
    species: str
    size_in: float
    notes: str


@dataclass
class RecordEntry:
    water_body: str
    species: str
    record_size_in: float


class FishingRepository:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        """Set up the repository and make sure the database is ready to use."""
        self.db_path = db_path
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        """Open a fresh connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    @staticmethod
    def _date_filter(start_date: Optional[str], end_date: Optional[str]) -> tuple[list, list]:
        """Build the WHERE conditions and params list for optional date range filtering."""
        conditions: list = []
        params: list = []
        if start_date:
            conditions.append("date(catch_date) >= date(?)")
            params.append(start_date)
        if end_date:
            conditions.append("date(catch_date) <= date(?)")
            params.append(end_date)
        return conditions, params

    def _initialize_database(self) -> None:
        """Make sure the db folder and catches table exist before anything else runs."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        with self._connect() as conn:
            conn.executescript(schema_sql)
        self._migrate_legacy_catches_table()

    def _migrate_legacy_catches_table(self) -> None:
        """Upgrade older catches tables to the current schema without quantity and with required size."""
        with self._connect() as conn:
            columns = {
                row[1]: row for row in conn.execute("PRAGMA table_info(catches)").fetchall()
            }

            has_quantity = "quantity" in columns
            has_size = "size_in" in columns
            size_required = bool(columns.get("size_in", (None, None, None, None, None, 0))[3])

            if not has_quantity and has_size and size_required:
                return

            conn.executescript(
                """
                BEGIN;
                ALTER TABLE catches RENAME TO catches_old;
                CREATE TABLE catches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    catch_date TEXT NOT NULL,
                    water_body TEXT NOT NULL,
                    county TEXT NOT NULL,
                    species TEXT NOT NULL,
                    size_in REAL NOT NULL CHECK (size_in > 0),
                    notes TEXT
                );
                INSERT INTO catches (id, catch_date, water_body, county, species, size_in, notes)
                SELECT
                    id,
                    catch_date,
                    water_body,
                    county,
                    species,
                    CASE
                        WHEN size_in IS NULL OR size_in <= 0 THEN 1.0
                        ELSE size_in
                    END,
                    notes
                FROM catches_old;
                DROP TABLE catches_old;
                COMMIT;
                """
            )

    def add_catch(
        self,
        catch_date: str,
        water_body: str,
        county: str,
        species: str,
        size_in: float,
        notes: str,
    ) -> None:
        """Save a new fishing catch to the database."""
        sql = """
        INSERT INTO catches (catch_date, water_body, county, species, size_in, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            conn.execute(
                sql,
                (catch_date, water_body.strip(), county.strip(), species.strip(), size_in, notes.strip()),
            )

    def update_catch(
        self,
        catch_id: int,
        catch_date: str,
        water_body: str,
        county: str,
        species: str,
        size_in: float,
        notes: str,
    ) -> None:
        """Overwrite the fields of an existing catch by its id."""
        sql = """
        UPDATE catches
        SET catch_date = ?, water_body = ?, county = ?, species = ?, size_in = ?, notes = ?
        WHERE id = ?
        """
        with self._connect() as conn:
            conn.execute(
                sql,
                (catch_date, water_body.strip(), county.strip(), species.strip(), size_in, notes.strip(), catch_id),
            )

    def delete_catch(self, catch_id: int) -> None:
        """Remove a catch record by its id."""
        sql = "DELETE FROM catches WHERE id = ?"
        with self._connect() as conn:
            conn.execute(sql, (catch_id,))

    def list_catches(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[CatchRecord]:
        """Fetch all catches, newest first. Optionally narrows results to a date range."""
        conditions, params = self._date_filter(start_date, end_date)
        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        sql = f"""
        SELECT id, catch_date, water_body, county, species, size_in, COALESCE(notes, '')
        FROM catches
        {where_clause}
        ORDER BY date(catch_date) DESC, id DESC
        """

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [CatchRecord(*row) for row in rows]

    def total_catches(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> int:
        """Count catches in the current date range."""
        conditions, params = self._date_filter(start_date, end_date)
        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        sql = f"""
        SELECT COUNT(*)
        FROM catches
        {where_clause}
        """

        with self._connect() as conn:
            total_count = conn.execute(sql, params).fetchone()[0]

        return int(total_count)

    def get_records(
        self,
        water_body: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[RecordEntry]:
        """Find the biggest fish per species. Leave water_body blank for state-wide records."""
        conditions, params = self._date_filter(start_date, end_date)
        conditions.insert(0, "size_in IS NOT NULL")

        if water_body:
            conditions.append("water_body = ?")
            params.append(water_body)

        where_clause = "WHERE " + " AND ".join(conditions)

        # Scope to one water body when provided, otherwise collapse across all waters for state records.
        if water_body:
            select_water = "water_body"
            group_by = "GROUP BY water_body, species"
        else:
            select_water = "'All Waters'"
            group_by = "GROUP BY species"

        sql = f"""
        SELECT {select_water}, species, MAX(size_in)
        FROM catches
        {where_clause}
        {group_by}
        ORDER BY species ASC, MAX(size_in) DESC
        """

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [RecordEntry(water_body=row[0], species=row[1], record_size_in=row[2]) for row in rows]
