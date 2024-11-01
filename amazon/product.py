import time
from types import TracebackType
from typing import Type
import sqlite3
from datetime import datetime

class Product():
    def __init__(self, review_count=None, rating=None, sentiment=None, title=None,current_price=None, last_known_price=None, discount=None, product_link=None, image=None, date_last_update=None, brand=None, search_term = None, lowest_price=None, sentiment_array = None):
        self.title = title
        self.current_price = current_price
        self.last_known_price = last_known_price
        self.discount = discount
        self.product_link = product_link
        self.image = image
        self.date_last_update = datetime.now().date()
        self.brand = brand
        self.search_term = search_term
        self.sentiment = sentiment
        self.rating = rating
        self.review_count = review_count
        self.sentiment_array = sentiment_array
        
        
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        self.quit()
        
    def save(self):
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
       
        # Check if the product already exists
        c.execute("SELECT * FROM products WHERE title=?", (self.title,))
        existing_product = c.fetchone()
        if existing_product:
            c.execute("""UPDATE products SET 
            current_price=?, last_known_price=?, discount=?, 
            product_link=?, image=?, date_last_update=?, 
            brand=?, search_term=?, sentiment=?, rating=?, review_count=?, sentiment_array=? WHERE title=?""",
            (self.current_price, self.last_known_price, self.discount,
            self.product_link, self.image, self.date_last_update,
            self.brand, self.search_term, self.sentiment, self.rating, self.review_count, self.sentiment_array, self.title))
        else:
            # Insert a new product
            c.execute("""INSERT INTO products 
                         (title, current_price, last_known_price, discount, 
                         product_link, image, date_last_update, brand, search_term, sentiment, rating, review_count, sentiment_array) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (self.title, self.current_price, self.last_known_price,
                       self.discount, self.product_link, self.image,
                       self.date_last_update, self.brand, self.search_term, self.sentiment, self.rating, self.review_count, self.sentiment_array))
        conn.commit()
        conn.close()
        
    
    def record_price_history(self):
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        
        recorded_date = datetime.now().date()
        row = c.execute("SELECT id FROM products WHERE title=?", (self.title,)).fetchone()

        # Check if a result was returned
        if row:
            product_id = row[0]
            print(f"Product ID: {product_id}")
        else:
            print("No product found with the given title.")
        
        c.execute("""
            INSERT INTO PriceHistory (product_id, recorded_date, price)
            VALUES (?, ?, ?)
        """, (product_id, recorded_date, self.current_price))
        conn.commit()

