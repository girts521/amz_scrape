from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pdb  
from amazon.amazon import Amazon
import sqlite3
from datetime import datetime

class Phone:
    def __init__(self, id, title, current_price, discount, product_link, image, date_last_update, brand, search_term):
        self.id = id
        self.title = title
        self.current_price = current_price
        self.discount = discount
        self.product_link = product_link
        self.image = image
        self.date_last_update = date_last_update
        self.brand = brand
        self.search_term = search_term

    def __repr__(self):
        return f"Product(id={self.id}, title={self.title}, current_price={self.current_price}, discount={self.discount}, product_link={self.product_link}, image={self.image}, date_last_update={self.date_last_update}, brand={self.brand}, search_term={self.search_term})"



with Amazon() as bot:
    bot.land_page(url='https://www.gsmarena.com/')
    time.sleep(1)
    conn = sqlite3.connect('products.db')
    conn_phones = sqlite3.connect('phones.db')
    c = conn.cursor()
    c_phones = conn_phones.cursor()
    
    c.execute("SELECT * FROM products WHERE search_term = 'smartphone'")
    products_data = c.fetchall()
    
    products = []
    for item in products_data:
        product = Phone(
            id=item[0],
            title=item[1],
            current_price=item[2],
            discount=item[4],
            product_link=item[5],
            image=item[6],
            date_last_update=item[7],
            brand=item[8],
            search_term=item[9]
        )
        products.append(product)
    for product in products:
        search = bot.find_element(By.CSS_SELECTOR, '#topsearch-text')
        model_parts = product.brand.split("_")
        model = ""
        if len(model_parts) > 1 and model_parts[1]:
            model = model_parts[1]
        print(f"model: {model}")
        search.clear()
        search.send_keys(model)
        search.send_keys(Keys.ENTER)
        time.sleep(1)
        result_num = 1
        try:
            result_text = bot.find_element(By.CSS_SELECTOR,f'#review-body > div > ul > li:nth-child({result_num}) > a > strong > span').get_attribute("innerHTML").replace("<br>", " ")
            result = bot.find_element(By.XPATH, f'//*[@id="review-body"]/div/ul/li[{result_num}]/a')
        except:
            continue


        while result_text != model and result_text != product.brand.replace("_", " ") and result_num != 10:
            try:
                print(result_text, model)
                print(result_text, product.brand)
                print("num: ", result_num)
                result_text = bot.find_element(By.CSS_SELECTOR,f'#review-body > div > ul > li:nth-child({result_num}) > a > strong > span').get_attribute("innerHTML").replace("<br>", " ")
                result = bot.find_element(By.XPATH, f'//*[@id="review-body"]/div/ul/li[{result_num}]/a')
                result_num = result_num + 1
            except:
                result = None
                break
        if result == None:
            continue
        result.click()
        time.sleep(1)
        try:
            release_date = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="status"]').text
        except:
            release_date = ""
        try:
            dimensions = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="dimensions"]').text
        except:
            dimensions = ""
        try:
            weight = bot.find_element(By.CSS_SELECTOR,'td[data-spec="weight"]').text
        except:
            weight = ""
        try:
            build = bot.find_element(By.CSS_SELECTOR,'td[data-spec="build"]').text
        except:
            build = ""
        try:
            sim = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="sim"]').text
        except:
            sim = ""
        try:
            display_type = bot.find_element(By.CSS_SELECTOR,'td[data-spec="displaytype"]').text
        except:
            display_type = ""
        try:
            display_size = bot.find_element(By.CSS_SELECTOR,'td[data-spec="displaysize"]').text
        except:
            display_size = ""
        try:
            display_resolution = bot.find_element(By.CSS_SELECTOR,'td[data-spec="displayresolution"]').text
        except:
            display_resolution = ""
        try:
            os = bot.find_element(By.CSS_SELECTOR,'td[data-spec="os"]').text
        except:
            os = ""
        try:
            cpu = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="chipset"]').text
        except:
            cpu = ""
        try:
            gpu = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="gpu"]').text
        except:
            gpu = ""
        try:
            memory = bot.find_element(By.CSS_SELECTOR,'td[data-spec="internalmemory"]').text
        except:
            memory = ""
        try:
            main_camera = bot.find_element(By.CSS_SELECTOR,'td[data-spec="cam1modules"]').text
        except:
            main_camera = ""
        try:
            video = bot.find_element(By.CSS_SELECTOR, 'td[data-spec="cam1video"]').text
        except:
            video = ""
        try:
            selfie_camera = bot.find_element(By.CSS_SELECTOR,'td[data-spec="cam2modules"]').text
        except:
            selfie_camera = ""
        try: 
            sensors = bot.find_element(By.CSS_SELECTOR,'td[data-spec="sensors"]').text
        except:
            sensors = ""
        try:
            battery_type = bot.find_element(By.CSS_SELECTOR,'td[data-spec="batdescription1"]').text
        except:
            battery_type = ""
        print(f'''
        release_date: {release_date},
        dimensions: {dimensions},
        weight: {weight},
        build: {build},
        sim: {sim},
        display_type: {display_type},
        display_size: {display_size},
        display_resolution: {display_resolution},
        os: {os},
        cpu: {cpu},
        gpu: {gpu},
        memory: {memory},
        main_camera: {main_camera},
        video: {video},
        selfie_camera: {selfie_camera},
        sensors: {sensors},
        battery_type: {battery_type}
        ''')
        
        c_phones.execute('''
        INSERT OR REPLACE INTO products(
            id, title, current_price, discount, product_link, image, date_last_update, brand, search_term,
            release_date, dimensions, weight, build, sim, display_type, display_size, display_resolution, os, 
            cpu, gpu, memory, main_camera, video, selfie_camera, sensors, battery_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.id, product.title, product.current_price, product.discount, product.product_link, product.image, 
            product.date_last_update, product.brand, product.search_term, release_date, dimensions, weight, build, sim, 
            display_type, display_size, display_resolution, os, cpu, gpu, memory, main_camera, video, 
            selfie_camera, sensors, battery_type
        ))
        
        conn_phones.commit()
        
        bot.back()
        bot.back()
        time.sleep(3)

    print("Done!")
    time.sleep(3)
    print("Exiting...")