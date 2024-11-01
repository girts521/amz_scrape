CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    current_price REAL,
    last_known_price REAL,
    discount REAL,
    product_link TEXT,
    image TEXT,
    date_last_update TEXT,
    brand TEXT,
    search_term TEXT
);