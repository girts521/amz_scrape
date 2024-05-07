from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import amazon.constants as const

import time
from types import TracebackType
from typing import Type

class Amazon(webdriver.Chrome):
    def __init__(self, options=None, *args, **kwargs):
        if options is None:
            options = Options()
            # options.add_argument("--headless=new")
        super().__init__(options=options, *args, **kwargs)
        self.implicitly_wait(15)
        self.actions = ActionChains(self)
    
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        self.quit()

    def land_page(self):
        self.get(const.BASE_URL)
        time.sleep(5)

    def remove_cookie_banner(self):
        try:
            cookie_banner = self.find_element(By.ID, "sp-cc-rejectall-link")
            cookie_banner.click()
            return True
        except NoSuchElementException:
            print("Cookie banner not found, moving on.")
            return False



    def select_category(self, category=None):
        self.refresh() 
        time.sleep(1)
        print("Trying to find the category input")
        categoryInput = self.find_element(By.ID, "searchDropdownBox")
        # categoryInput = WebDriverWait(self,20).until(
        #     EC.element_to_be_clickable((
        #         By.ID,
        #         "searchDropdownBox"
        #     ))
        # )
        print("Clicking on category input")
        categoryInput.click()
        time.sleep(1)
        # category_option = categoryInput.find_element(By.XPATH, f'//option[contains(text(), "{category}")]')
        # print("Clicking on the category")
        # # category_option.click()
        # category_option.__setattr__("selected", True)
        # time.sleep(1)
    
    def input_search(self, search=None):
        self.refresh()
        time.sleep(1)
        print("Selecting the search field")

        search_field = WebDriverWait(self, 20).until(
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
        time.sleep(2)

    def next_page(self):
        self.refresh()
        print("Scrolling...")
        # self.actions.move_by_offset(0, 800).perform()
        self.execute_script('window.scrollBy({top: 10000,behavior: "smooth"});')
        time.sleep(3)
        try:
            next_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//span["s-pagination-strip"]/a[contains(text(), "Weiter")]'
                ))
            )
        except TimeoutException:
            self.execute_script('window.scrollBy({top: -1000,behavior: "smooth"});')
            next_button = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//span["s-pagination-strip"]/a[contains(text(), "Weiter")]'
                ))
            )
        time.sleep(1)
        print("Scrolling2...")
        # self.actions.move_to_element_with_offset(next_button, 10, 0).perform()
        print("Clicking to next page")
        time.sleep(3)
        next_button.click()
        

    def get_results(self):
        self.refresh()
        time.sleep(1)
        print("Selecting resuls on the page")
        results = WebDriverWait(self, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
            )
        )
        time.sleep(1)
        print("Found result ", results)
        time.sleep(2)

        for result in results:
            priceParent = result.find_element(By.CSS_SELECTOR, 'div[data-cy="price-recipe"]')
            price = priceParent.find_elements(By.CSS_SELECTOR, 'span.a-offscreen')
            title = result.find_element(By.CSS_SELECTOR, 'div[data-cy="title-recipe"] h2 a span').text
            image = result.find_element(By.CSS_SELECTOR, 'div.s-product-image-container img.s-image').get_attribute("src")
            print("image: ", image)
            if len(price) > 1:
                original_price = float(price[1].get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.'))
                new_price = float(price[0].get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.'))
                price_discount = ((original_price - new_price) / original_price) * 100
                print(price_discount)
                if price_discount > 80:
                    WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a')
                    )
                    )
                    time.sleep(1)
                    product_link = result.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a')
                    self.actions.move_to_element_with_offset(product_link, 50, 0)
                    print("Clicking the product link")
                    time.sleep(1)
                    product_link.click()
                    time.sleep(1)
                    url = self.current_url
                    print("url: ",url)
                    self.back()
                    time.sleep(3)
            
            # old_price_html = old_price_el.get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace(',', '.')
            
            

