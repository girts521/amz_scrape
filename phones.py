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
    bot.land_page(url='https://www.amazon.de/s?k=smartphone&i=electronics&rh=n%3A562066%2Cp_89%3AFairphone%7CGoogle%7CHONOR%7CHUAWEI%7CNothing%7COPPO%7CSamsung%7CTCL%7CXiaomi%7Crealme&dc&crid=3JG1R7K5ZF3ZA&qid=1716396962&rnid=669059031&sprefix=sma%2Celectronics%2C82&ref=sr_nr_p_89_21&ds=v1%3AnjOE7Kd33rNzQhUI3zbgF50LNlz85hOcOQhmJT0k9Kc')
    cookie_banner_removed = bot.remove_cookie_banner()
    time.sleep(2)
    # bot.input_search(search="smartphone")
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()

    
    num = 71
    while num != 0:
        bot.get_phone_ppd_results(search_term="smartphone")
        bot.next_page()
        num = num -1
        time.sleep(3)
    # pdb.set_trace()
    print("Done!")
    time.sleep(3)
    print("Exiting...")