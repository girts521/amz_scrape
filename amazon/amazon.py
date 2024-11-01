from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException
import amazon.constants as const
from amazon.product import Product
from amazon.alert import Alert
from helpers.helpers import scroll
from helpers.helpers import get_search_page_product_details
from helpers.helpers import get_product_details_on_ppd
from helpers.helpers import get_product_rating_on_ppd
from helpers.helpers import get_user_reviews
from helpers.helpers import get_sentiment
from helpers.helpers import get_phone_details
import pdb  
import json

import time
from types import TracebackType
from typing import Type

class Amazon(webdriver.Chrome):
    def __init__(self, options=None, *args, **kwargs):
        if options is None:
            options = Options()
        options.add_argument("--headless")
        super().__init__(options=options, *args, **kwargs)
        self.implicitly_wait(3)
        self.actions = ActionChains(self)
    
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        self.quit()

    def land_page(self, url=None):
        if url:
            self.get(url)
        else:
            self.get(const.BASE_URL)
        time.sleep(15)

    def remove_cookie_banner(self):
        try:
            cookie_banner = self.find_element(By.ID, "sp-cc-rejectall-link")
            cookie_banner.click()
            return True
        except NoSuchElementException:
            print("Cookie banner not found, moving on.")
            return False

    def select_category(self, categories=[]):
        self.refresh() 
        time.sleep(1)
        print("Click on 30%+ discount")
        discount = WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'div[data-testid="filter-percentOff-3"] label'
            ))
        )
        scroll(self, target=discount)
        time.sleep(1)
        discount.click()
       
    
    def input_search(self, search=None):
        self.refresh()
        time.sleep(1)
        print("Selecting the search field")

        search_field = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((
                By.ID,
                "twotabsearchtextbox"
            ))
        )
        print("Adding input: ", search)
        time.sleep(1)
        search_field.send_keys(search)
        search_field.send_keys(Keys.ENTER)
        time.sleep(2)

    def select_deals(self):
        print("Selecting deals only")
        try:
            deals = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((
                By.XPATH,
                '//span[contains(text(), "Tagesangebote")]'
                ))
            )
        except TimeoutException:
            deals = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((
                By.XPATH,
                '//span[contains(text(), "Alle Angebote")]'
                ))
            )
        print("Click on deal")
        deals.click()
        
    def select_brand(self, brand):
        print("Selecting brand: ", brand)
        el = self.find_element(By.CSS_SELECTOR, f'#brandsRefinements li[aria-label="{brand}"] > span > a')
        print("Clicking on brand")
        time.sleep(1)
        el.click()

    def next_page(self):
        self.refresh()
        print("Scrolling...")
        scroll(self, distance=11000)
        time.sleep(1)
        try:
            next_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//span["s-pagination-strip"]/a[contains(text(), "Weiter")]'
                ))
            )
        except TimeoutException:
            print("Scrolling2...")
            scroll(self, distance=-1000)
            next_button = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '.a-pagination .a-last a'
                ))
            )
        time.sleep(1)
        print("Clicking to next page")
        next_button.click()
        
        
    def get_phone_ppd_results(self, search_term=None):
        self.refresh()
        print("Selecting resuls on the page")
        results = WebDriverWait(self, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
            )
        )
        print("Found result ", len(results))
        for index, result in enumerate(results):
            print("Index: ",index )
            product_link = result.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a')
            product_link.click()
            get_phone_details(self, search_term=search_term)

# #######################################################################################################
    def get_search_page_general_results(self, get_brand=False,set_brand=None, search_term=None):
        self.refresh()
        print("Selecting resuls on the page")
        results = WebDriverWait(self, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
            )
        )
        print("Found result ", len(results))
        for index, result in enumerate(results):
            print("Index: ",index )
            new_product = get_search_page_product_details(self, result=result, get_brand=get_brand)
            if search_term:
                new_product.search_term = search_term
            if set_brand:
                print("Setting brand: ", set_brand)
                new_product.brand = set_brand
            if new_product.discount and new_product.discount > 20:
                print("Clicking on product")
                try:
                    product_link = result.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a')
                except:
                    print("Bad link: ", product_link )
                time.sleep(1)
                product_link.click()
                # get_product_details_on_ppd(self, search_term=search_term)
                rating, review_count = get_product_rating_on_ppd(self)
                print("rating: ", rating)
                print("review_count:", review_count)
                reviews = get_user_reviews(self)
                print("Reviews: ", reviews)
                # pdb.set_trace()
                print("going back")
                self.back()
                time.sleep(1)
                print(len(reviews))
                if len(reviews) > 0:
                    self.back()
                time.sleep(1)
                new_product.rating = rating
                new_product.review_count = review_count
                print("Getting sentiment")
                sentiment, filtered_result = get_sentiment(reviews)
                new_product.sentiment = sentiment
                json_string = json.dumps(filtered_result)
                new_product.sentiment_array = json_string
            print(f'product: {new_product.title}, sentiment: {new_product.sentiment}')
            new_product.save()
            new_product.record_price_history()


    def get_kitchen_bestsellers(self, get_brand=False,set_brand=None, search_term=None):
        self.refresh()
        time.sleep(1)
        print("Selecting resuls on the page")
        results = WebDriverWait(self, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '#gridItemRoot')
            )
        )
        print("Found result ", len(results))
        for index, result in enumerate(results):
            print("Index: ",index )
            product_link = result.find_element(By.CSS_SELECTOR, 'a.a-link-normal')
            print("Clicking on product")
            time.sleep(1)
            product_link.click()
            get_product_details_on_ppd(self, search_term=search_term)
            time.sleep(2)
            self.back()
            
    
    def get_more_products(self, search_term=None):
        products_container = self.find_elements(By.CSS_SELECTOR, "#octopus-dlp-asin-stream ul li")
        for product in products_container:
            product_link = product.find_element(By.CSS_SELECTOR, 'a.a-link-normal')
            product_link.click()
            time.sleep(2)
            ppd = self.find_element(By.CSS_SELECTOR, '#ppd #centerCol')
            if ppd:
                self.get_product_details_on_ppd(search_term=search_term)
            self.back()
            time.sleep(1)
    
    def get_products_infinite_scroll(self, visited_products):
        products_list = self.find_elements(By.CSS_SELECTOR, 'div[data-test-id="virtuoso-item-list"] > div')
        print("Found rows: ",len(products_list))
        row_index = 0
        while row_index < len(products_list) -1:
            try:
                product_id = products_list[row_index].get_attribute("data-item-index")
                print("id: ", product_id)
            except:
                pdb.set_trace()
            if product_id not in visited_products:
                products = products_list[row_index].find_elements(By.CSS_SELECTOR, 'div[data-test-id="virtuoso-item-list"] > div > div > div > div > div')
                for product in products:
                    time.sleep(1)
                    product_link = product.find_element(By.CSS_SELECTOR, "a.a-link-normal")
                    product_link.click()
                    try:
                        ppd = self.find_element(By.CSS_SELECTOR, '#ppd #centerCol')
                        if ppd:
                            get_product_details_on_ppd(self,search_term="deals")
                    except WebDriverException:
                        try:
                            self.get_more_products(self,search_term="deals")
                            try:
                                self.execute_script('window.scrollBy({top: 4000,behavior: "smooth"});')
                                pagination = self.find_element(By.CSS_SELECTOR, '#octopus-dlp-pagination .a-pagination .a-last')
                                pagination.click()
                                self.get_more_products(self,search_term="deals")
                            except WebDriverException:
                                print("No pages")
                                self.back()
                        except WebDriverException:
                            print("Error :(") 
                    visited_products.add(product_id)
                    print("visited_products: ", visited_products)
                    self.back() 
            row_index = row_index +1
            products_list = self.find_elements(By.CSS_SELECTOR, 'div[data-test-id="virtuoso-item-list"] > div')
            

        return visited_products
    
    def get_deals(self):
        print("Clicking on each product")
        visited_products = set()
        num = 10
        while num > 0:
            visited_products = self.get_products_infinite_scroll(visited_products=visited_products)
            print("Scrolling...")
            scroll(self, distance="1000")
            try:
                load_more_btn = self.find_element(By.CSS_SELECTOR, 'div[data-testid="load-more-footer"] > span')
                load_more_btn.click()
            except WebDriverException:
                continue
            time.sleep(2)
            num = num -1
