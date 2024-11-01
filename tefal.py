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
    bot.input_search(search="Tefal")
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.select_brand("Tefal")
    bot.select_deals()

    num = 11
    while num != 0:
        bot.get_search_page_general_results(get_brand=False, set_brand="Tefal", search_term="Tefal")
        bot.next_page()
        num = num -1
        time.sleep(3)
    # pdb.set_trace()
    print("Done!")
    time.sleep(3)
    print("Exiting...")