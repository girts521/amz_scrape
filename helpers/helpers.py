import pdb  
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException
from amazon.product import Product
import time
import re
import requests
import json
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
import pandas as pd

# Scrolls to target or for set distance
def scroll(self, distance=None, target=None):
    if target:
        self.execute_script('arguments[0].scrollIntoView(true);', target)
    elif distance:
        self.execute_script(f'window.scrollBy({{top: {distance}, behavior: "smooth"}});')


# gets product details from search page results
def get_search_page_product_details(self, result, get_brand):
    priceParent = result.find_element(By.CSS_SELECTOR, 'div[data-cy="price-recipe"]')
    try:
        price = priceParent.find_element(By.CSS_SELECTOR, 'span.a-price span.a-offscreen').get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.')
    except NoSuchElementException:
        price = "0"
    title = result.find_element(By.CSS_SELECTOR, 'div[data-cy="title-recipe"] h2 a span').text
    image = result.find_element(By.CSS_SELECTOR, 'div.s-product-image-container img.s-image').get_attribute("src")
    product_link = result.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a').get_attribute("href")
    if price:
        new_price = float(price)
    else:
        # Handle the case where price is empty
        new_price = 0.0  
    print("new price: ",new_price)
    new_product = Product(title=title, current_price=new_price, product_link=product_link, image=image)
    try:
        original_price = priceParent.find_element(By.XPATH, './/span[contains(text(), "Statt") or contains(text(), "UVP")]/following-sibling::span/span[contains(@class, "a-offscreen")]').get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.')
    except NoSuchElementException:
        original_price = None 
    # If discount then check the % and alert
    if original_price:
        original_price = float(original_price)
        print("original price: ", original_price)
        price_discount = ((original_price - new_price) / original_price) * 100
        new_product.discount = price_discount

    if get_brand == True:
        link = result.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] a')
        scroll(target=link)
        print("Clicking the product link")
        link.click()
        # Get the brand name
        print("Getting the brand name")
        brand = self.find_element(By.CSS_SELECTOR, '.po-brand .po-break-word').text
        print("Brand: ", brand)
        new_product.brand = brand
        self.back()
        time.sleep(2)
    return new_product

def get_price_on_ppd(self):
    try:
            price_whole = self.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div span.reinventPricePriceToPayMargin span[aria-hidden] span.a-price-whole').text.strip().replace('.',"")
            price_fraction = self.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div span.reinventPricePriceToPayMargin span[aria-hidden] span.a-price-fraction').text
            print("Got price: ", f"{price_whole}.{price_fraction}" )
    except NoSuchElementException:
        try:
            price_whole = self.find_element(By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr[2]/td[2]/span[1]/span[1]').get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.')
            price_fraction = ""
            print("Got price: ", f"{price_whole}.{price_fraction}" )
        except NoSuchElementException:
            try:
                price_whole = self.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr[1]/td[2]/span[1]/span[1]/span[1]').get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.')
                price_fraction = ""
                print("Got price: ", f"{price_whole}.{price_fraction}" )
            except NoSuchElementException:
                try:
                    price_whole = self.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[1]').get_attribute("innerHTML").replace("&nbsp;", "").replace("€", "").strip().replace('.',"").replace(',', '.')
                    price_fraction = ""
                    print("Got price: ", f"{price_whole}.{price_fraction}" )
                except NoSuchElementException:
                    price_whole = "0"
                    price_fraction = ""
                    pdb.set_trace()
                
    if len(price_fraction):
        print("whole:", price_whole)
        print("fraction: ", price_fraction)
        current_price = float(f"{price_whole}.{price_fraction}")
    else:
        current_price = float(f"{price_whole}")
    
    return current_price

def get_discount_on_ppd(self):
    try:
        print("Getting discount")
        discount = self.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div span.savingsPercentage')
        if discount.is_displayed():
            discount = discount.get_attribute("innerHTML").replace("&nbsp;", "").strip().replace('-',"").replace('%',"")
            print("Discount: ", discount)
        else:
            discount = self.find_element(By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr[3]/td[2]/span[1]/span')
            print("Discount with xpath: ", discount)    
    except NoSuchElementException:
        try:
            discount = self.find_element(By.XPATH,'//*[@id="corePrice_desktop"]/div/table/tbody/tr[3]/td[2]/span[1]').text
            match = re.search(r'\((\d+)\s?%\)', discount)
            if match:
                discount = match.group(1)
            else:
                discount = 0
                # pdb.set_trace()
        except NoSuchElementException:
            print("no element")
            discount = '0'
            # pdb.set_trace()
    return discount

def get_image_on_ppd(self):
    try:
        image = self.find_element(By.CSS_SELECTOR, '#imgTagWrapperId img').get_attribute("src")
    except NoSuchElementException:
        image = self.find_element(By.CSS_SELECTOR, 'div.imgTagWrapper > img').get_attribute("src")
    return image

def get_product_rating_on_ppd(self):
    try:
        parent = self.find_element(By.CSS_SELECTOR, '#averageCustomerReviews')
        rating = parent.find_element(By.CSS_SELECTOR, '#acrPopover a span').text
        review_count_el = parent.find_element(By.CSS_SELECTOR, '#acrCustomerReviewText')
        match = re.search(r'\d+(\.\d+)?', review_count_el.text)
        if match:
            review_count = match.group(0)
        return {rating, review_count}
    except :
        print("failed to get rating returning 0")
        return 0,0

def get_user_reviews(self):
    result = []
    page_count = 0
    
    try:
        rating_btn = self.find_element(By.CSS_SELECTOR, '#acrCustomerReviewText')
        rating_btn.click()
        time.sleep(1)
        more_reviews_btn = self.find_element(By.CSS_SELECTOR, '#reviews-medley-footer > div.a-row.a-spacing-medium > a')
        more_reviews_btn.click()
        time.sleep(2)
        while True:
            try:
                print("Fetching reviews")
                # Fetch reviews
                reviews = self.find_elements(By.CSS_SELECTOR, "#cm_cr-review_list > div.review > div > div > div > span > span")
                time.sleep(2)
                result.extend(review.text for review in reviews)  # Use extend to add multiple elements
                print("Reviews count: ", len(result))
            except Exception as e:
                print("Error fetching more reviews:", str(e))
                break  # Exit the loop if there's an error finding the button or fetching reviews

            # Check for pagination
            try:
                next_page_button = self.find_element(By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul > li.a-last > a")
                print("Next page button found, continuing to next page.")
                time.sleep(2)
                next_page_button.click()
                page_count = page_count + 1
                time.sleep(4)
            except Exception:
                print("Next page button not found. No more reviews to load.")
                break  # Exit the loop if no more pages are available

    except Exception as e:
        print("An error occurred:", str(e))
    
    # Handle no reviews found
    if not result:
        print("No reviews found")
        result.append('No reviews yet.')
    while page_count >= 0:
        self.back()
        page_count = page_count -1
    print("Returning the results")
    return result


def get_sentiment(reviews):
    # Load pre-trained BERT model and tokenizer
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    device = 0 if torch.cuda.is_available() else -1 
    nlp = pipeline("sentiment-analysis", 
               model=model, 
               tokenizer=tokenizer, 
               device=device, 
               max_length=512, 
               truncation=True)
    filtered_reviews = [review for review in reviews if review.strip() and review != "Melden"]
    results = nlp(filtered_reviews)
    filtered_result = [result for result in results if result['score'] > 0.55]
    print("filtered result: ", filtered_result)

    df = pd.DataFrame(results)

    sentiment_mapping = {
    '5 stars': 'positive',
    '4 stars': 'positive',
    '3 stars': 'neutral',
    '2 stars': 'negative',
    '1 star': 'negative'
    }

    df['sentiment'] = df['label'].map(sentiment_mapping)
    sentiment_counts = df['sentiment'].value_counts()
    overall_sentiment = sentiment_counts.idxmax()

    return overall_sentiment, filtered_result

# gets product details on the product page
def get_product_details_on_ppd(self, search_term=None):
        ppd = self.find_element(By.CSS_SELECTOR, '#ppd #centerCol')
        print("Found ppd, getting title...")
        title = ppd.find_element(By.CSS_SELECTOR, '#productTitle').text
        current_price = get_price_on_ppd(self)     
        discount = get_discount_on_ppd(self)
        try:
            image = get_image_on_ppd(self)
        except:
            pdb.set_trace()
        try:
            brand = self.find_element(By.CSS_SELECTOR, '.po-brand .po-break-word').text
            print(brand)
        except NoSuchElementException:
            brand=None
        new_product = Product(title=title, current_price=current_price, product_link=self.current_url, image=image, brand=brand, search_term=search_term, discount=discount)
        new_product.save()
        self.back()
        time.sleep(2)
        
       
def get_phone_details(self, search_term=None, extra_phone=False):
        ppd = self.find_element(By.CSS_SELECTOR, '#ppd #centerCol')
        print("Found ppd, getting title...")
        title = ppd.find_element(By.CSS_SELECTOR, '#productTitle').text
        current_price = get_price_on_ppd(self)     
        discount = get_discount_on_ppd(self)
        image = get_image_on_ppd(self)
        try:
            brand = self.find_element(By.CSS_SELECTOR, '.po-brand .po-break-word').text
      
        except NoSuchElementException:
            brand=None
        
        try:
            model = self.find_element(By.CSS_SELECTOR, '.po-model_name .po-break-word').text
            print("model: ", model)
        except:
            model= ''

        brand = f'{brand}_{model}'
        
        print("brand + model:", brand)
        new_product = Product(title=title, current_price=current_price, product_link=self.current_url, image=image, brand=brand, search_term=search_term, discount=discount)
        new_product.save()
        self.back()
        time.sleep(2)
        