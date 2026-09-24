
CREATE TABLE IF NOT EXISTS restaurants (
    place_id            TEXT PRIMARY KEY,
    title               TEXT NOT NULL,
    category_name       TEXT NOT NULL,
    category_primary    TEXT,

    address             TEXT,
    city_raw            TEXT,
    city_clean          TEXT,
    neighborhood        TEXT,
    street              TEXT,
    postal_code         INTEGER,
    latitude            REAL,
    longitude           REAL,

    total_score         REAL,
    reviews_count       INTEGER NOT NULL DEFAULT 0,
    is_rated            INTEGER NOT NULL,
    reviews_five_star   INTEGER DEFAULT 0,
    reviews_four_star   INTEGER DEFAULT 0,
    reviews_three_star  INTEGER DEFAULT 0,
    reviews_two_star    INTEGER DEFAULT 0,
    reviews_one_star    INTEGER DEFAULT 0,

    phone               TEXT,
    website             TEXT,

    open_status          TEXT,
    permanently_closed    INTEGER DEFAULT 0,
    temporarily_closed    INTEGER DEFAULT 0,

    search_string        TEXT,
    rank_in_search        INTEGER,
    scraped_at            TEXT,
    images_count           INTEGER DEFAULT 0,
    maps_url               TEXT
);
