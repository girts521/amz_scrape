import sqlite3

# Create a connection to the database
conn = sqlite3.connect('phones.db')

# Create a cursor object
c = conn.cursor()

# Create the unified table
c.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    title TEXT,
    current_price REAL,
    discount REAL,
    product_link TEXT,
    image TEXT,
    date_last_update DATE,
    brand TEXT,
    search_term TEXT,
    release_date TEXT,
    dimensions TEXT,
    weight TEXT,
    build TEXT,
    sim TEXT,
    display_type TEXT,
    display_size TEXT,
    display_resolution TEXT,
    os TEXT,
    cpu TEXT,
    gpu TEXT,
    memory TEXT,
    main_camera TEXT,
    video TEXT,
    selfie_camera TEXT,
    sensors TEXT,
    battery_type TEXT
)
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()