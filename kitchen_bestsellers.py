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
    bot.land_page(url="https://www.amazon.de/gp/bestsellers/kitchen/")
    
    cookie_banner_removed = bot.remove_cookie_banner()
    time.sleep(3)
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.get_kitchen_bestsellers(search_term="kitchen_bestsellers")
    bot.next_page()
    bot.get_kitchen_bestsellers(search_term="kitchen_bestsellers")
    # pdb.set_trace()
    print("Done!")
    time.sleep(13)
    print("Exiting...")