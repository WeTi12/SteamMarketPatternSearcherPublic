import json
import re
from message_sender import message_sender
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#load item data from file
print("scraping script started")
data = ""
with open("item.txt") as f:
    data = f.read()

data = json.loads(data)

if type(data) == dict:
    data = [data]

#open browser
options = Options() 
options.add_argument("-headless")
options.page_load_strategy = 'eager'
options.set_preference("permissions.default.image", 2)
driver = webdriver.Firefox(options)

for item in data:
    #getting inspect links and prices
    baseurl = item["link"]
    driver.get(baseurl)
    btns = driver.find_elements(By.CLASS_NAME, "market_actionmenu_button")
    inspect_links = None
    listing_ids = None
    prices = None
    patterns = None
    inspect_links = []
    listing_ids = []
    prices = []
    patterns = []
    print("Scraping button links")
    for btn in btns:
        id_of_listing = btn.get_attribute('id')
        listing_ids.append(id_of_listing)
        driver.execute_script("arguments[0].click();", btn)
        popup = driver.find_element(By.CSS_SELECTOR, "#market_action_popup_itemactions > a")
        href = popup.get_attribute('href')
        inspect_links.append(href)
        del href
        del popup
        del id_of_listing
    
    #release data from memory
    del btns

    #getting prices
    print("Scraping prices")
    pric = driver.find_elements(By.CLASS_NAME, "market_listing_price_with_fee")
    for pri in pric:
        pr = pri.text
        prices.append(pr)
        del pr

    #release data from memory
    del pric

    #getting patterns
    print("Scraping patterns")
    baseurl = "https://csfloat.com/checker"
    driver.get(baseurl)
    for link in inspect_links:
        input_to = driver.find_element(By.ID, "mat-input-1")
        a_index = link.find("A")
        print("getting pattern of item " + item["link"][47:] + " " + link[66:a_index+1])
        input_to.clear()
        input_to.send_keys(link)
        input_to.send_keys(Keys.ENTER)
        #get pattern
        try:
            details_div = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "item-props")))
            pattern = details_div.text[11:16]
            pattern = re.sub("[^0-9]", "", pattern)
            del details_div
            if len(pattern) == 0:
                print("Couldn't scrape item pattern, FloatDB error/slow internet issue")
            else:
                print(pattern)
            patterns.append(pattern)
            del pattern
        except TimeoutException:
            print("Loading took too much time!")
            pattern = ""
            patterns.append(pattern)
            del pattern
        
        del input_to
        driver.refresh()

    for i in range(0, len(inspect_links)):
        if patterns[i] in item["patterns"]:
            #load email data from file
            print("Pattern found, sending message")
            message_sender(item, patterns[i], prices[i], listing_ids[i], inspect_links[i])
            print(patterns[i], prices[i], listing_ids[i], item["link"], inspect_links[i])
            #remove item or patternfrom list and file if found
            if len(item["patterns"]) > 1:
                item["patterns"].remove(patterns[i])
                f = open("item.txt", "w")
                f.write(json.dumps(data))
                f.close()
            else:
                data.remove(item)
                f = open("item.txt", "w")
                f.write(json.dumps(data))
                f.close()
            print("Item removed")
            
#close browser
print("releasing memory")
driver.quit()
