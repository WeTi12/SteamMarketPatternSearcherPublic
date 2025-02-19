from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_pattern_info_old(items):
    print("----- Scraping patterns -----")
    #open browser
    options = Options() 
    options.add_argument("-headless")
    options.add_argument("-disable-infobars")
    options.add_argument("-disable-extensions")
    options.add_argument('-disable-application-cache')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-gpu')
    options.add_argument("-disable-dev-shm-usage")
    options.set_preference("permissions.default.image", 2)
    driver = webdriver.Firefox(options)

    patterns = []
    pattern = -1
    #getting patterns
    baseurl = "https://csfloat.com/checker"
    driver.get(baseurl)
    for link in items["inspect_links"]:
        input_to = driver.find_element(By.CLASS_NAME, "mat-mdc-input-element")
        a_index = link.find("A")
        print("Getting pattern of item: " + items["name"][0] + ", " + link[66:a_index+1])
        input_to.clear()
        input_to.send_keys(link)
        input_to.send_keys(Keys.ENTER)
        #get pattern
        try:
            details_div = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "table")))
            pattern_element = details_div.find_element(By.CLASS_NAME, "value")
            pattern = pattern_element.text
            del details_div
            if pattern == -1:
                print("Couldn't scrape item pattern, FloatDB error/slow internet issue")
            else:
                print(pattern)
            patterns.append(pattern)
            pattern = -1
        except TimeoutException:
            print("Loading took too much time! --> This is most likely due to csfloat still processing this item")
            pattern = ""
            patterns.append(pattern)
            pattern = -1
        
        del input_to
        driver.refresh()

    #close browser
    print("releasing memory")
    del pattern
    driver.quit()

    return patterns