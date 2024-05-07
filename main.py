from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pdb  
from amazon.amazon import Amazon

with Amazon() as bot:
    bot.land_page()
    cookie_banner_removed = bot.remove_cookie_banner()
    # bot.select_category(category="Angebote")
    bot.input_search(search="laptop")
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.get_results()
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.next_page()
    bot.get_results()
    bot.next_page()
    bot.get_results()
    bot.next_page()
    bot.get_results()
    # pdb.set_trace()
    print("Done!")
    time.sleep(3)
    print("Exiting...")