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
    bot.land_page(url="https://www.amazon.de/deals")
    cookie_banner_removed = bot.remove_cookie_banner()
    time.sleep(1)
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
   
#    Select categories: Amazon-Geräte, Drogerie & Körperpflege, Elektro-Großgeräte, Elektronik & Foto, Koffer, Rucksäcke & Taschen, Kosmetik, Küche, Haushalt & Wohnen, 30 % Rabatt oder mehr, Alle Angebote
    bot.select_category(['Amazon-Geräte', 'Drogerie & Körperpflege', 'Elektro-Großgeräte', 'Elektronik & Foto', 'Koffer, Rucksäcke & Taschen', 'Kosmetik', 'Küche', 'Haushalt & Wohnen'])
    if cookie_banner_removed == False:
        cookie_banner_removed = bot.remove_cookie_banner()
    bot.get_deals()
    print("Done!")
    pdb.set_trace()

    time.sleep(30)
    print("Exiting...")
    
    
    