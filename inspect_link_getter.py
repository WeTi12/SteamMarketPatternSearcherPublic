import time
import json
import smtplib
import datetime
import re
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

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
driver = webdriver.Firefox(options)

for item in data:
    #getting inspect links and prices
    baseurl = item["link"]
    driver.get(baseurl)
    btns = driver.find_elements(By.CLASS_NAME, "market_actionmenu_button")
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
            details_div = WebDriverWait(driver, 1.2).until(EC.presence_of_element_located((By.CLASS_NAME, "item-props")))
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
        
        driver.refresh()

    for i in range(0, len(inspect_links)):
        if patterns[i] in item["patterns"]:
            #load email data from file
            print("Pattern found, sending message")
            datenow = datetime.datetime.now()
            email_data = ""
            with open("details.txt") as f:
                email_data = f.readlines()
            message = "Item found: "
            message += item["name"]
            message += "\n"
            message += "Date: "
            message += datenow.strftime("%Y-%m-%d %H:%M:%S")
            message += " "
            message += item["link"]
            message += "\npattern found: "
            message += patterns[i]
            message += "\nprice: "
            message += prices[i]
            message += "\nadditional info: "
            message += listing_ids[i]
            message += "\ninspect link: "
            message += inspect_links[i]
            title = "Item found " + item["name"] + " " + datenow.strftime("%Y-%m-%d %H:%M:%S")
            send_email(title, message, email_data[0], email_data[2].split(","), email_data[1])
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
driver.quit()
