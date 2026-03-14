CREATE TABLE IF NOT EXISTS catches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    catch_date TEXT NOT NULL,
    water_body TEXT NOT NULL,
    county TEXT NOT NULL,
    species TEXT NOT NULL,
    size_in REAL NOT NULL CHECK (size_in > 0),
    notes TEXT
);
