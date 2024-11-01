from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pdb  
from amazon.amazon import Amazon
from amazon.alert import Alert

with Amazon() as bot:
    bot.land_page()
    cookie_banner_removed = bot.remove_cookie_banner()
    bot.input_search(search="laptop")
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.get_general_results(get_brand=True, search_term="laptop")
    print("Done!")
    time.sleep(3)
    print("Exiting...")