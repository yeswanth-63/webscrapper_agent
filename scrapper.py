from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

PRODUCT_URLS = {
        "laptops": "https://webscraper.io/test-sites/e-commerce/static/computers/laptops",
        "tablets": "https://webscraper.io/test-sites/e-commerce/static/computers/tablets",
        "touch": "https://webscraper.io/test-sites/e-commerce/static/phones/touch"
}



def scrape_subcategory(subcategory: str, keyword: str = None, max_price: float = None, max_pages: int = 5):
    url = PRODUCT_URLS.get(subcategory.lower())
    if not url:
        print("[ERROR] No URL found for subcategory:", subcategory)
        return pd.DataFrame()

    print(f"[SCRAPER START] Subcategory: {subcategory}, URL: {url}, Keyword: {keyword}, Max Price: {max_price}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    all_data = []
    page = 1

    while page <= max_pages:
        page_url = f"{url}?page={page}"
        driver.get(page_url)

        try:
            products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.thumbnail")))
        except:
            break  # No more pages

        if not products:
            break

        for product in products:
            try:
                name = product.find_element(By.CLASS_NAME, "title").text
                price = product.find_element(By.CLASS_NAME, "price").text
                desc = product.find_element(By.CLASS_NAME, "description").text
                all_data.append([name, price, desc])
            except:
                continue

        print(f"✅ Scraped {len(products)} products from page {page}")
        page += 1
        time.sleep(1)

    driver.quit()
    df=pd.DataFrame(all_data, columns=["Product Name", "Price", "Description"])
        # Clean price column
    df["Price"] = df["Price"].replace('[\$,]', '', regex=True).astype(float)

    # Apply filter if max_price is given
    if max_price is not None:
        df = df[df["Price"] <= max_price]

    return df
    # print(len(all_data))
    # return pd.DataFrame(all_data, columns=["Product Name", "Price", "Description"])





