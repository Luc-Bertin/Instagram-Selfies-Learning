from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import regex as re
import getpass
import requests
import os
import sys
import time

import credentials
from decorators import NbCallFunction

# Options for the web driver (here incognito mode for Chrome, optional)
options = webdriver.ChromeOptions()
options.add_argument(' — incognito')
# Get the webdriver from its location path
driver = webdriver.Chrome(executable_path='/Users/lucbertin/Desktop/chromedriver', options = options)
# Go to Instagram main connection page
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
timeout = 10

# Handling TimeOutException if connection is bad or even nonxistent
try:
    WebDriverWait(driver, timeout).until(ec.visibility_of_all_elements_located((By.TAG_NAME, 'input')))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()
    sys.exit(1)

# Enter ID/password
driver.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys(credentials.USER_ID)
driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(credentials.USER_PASSWORD)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Handle this fucking pop-up while opening Instagram
try:
    WebDriverWait(driver, timeout).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']")))
    driver.find_element(By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']").click()
except NoSuchElementException:
    print("Actually, there wasn't any pop up to activate notifications")
    driver.quit()
    sys.exit(1)

faceportrait = "#faceportrait"
search_bar = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Rechercher']")
search_bar.send_keys(faceportrait)
time.sleep(3)
search_bar.send_keys(Keys.ENTER)
search_bar.send_keys(Keys.ENTER)

# All photos that appeared or will appear are located in div[class='v1Nh3 kIKUG  _bz0w']
try: 
    WebDriverWait(driver, timeout).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w']")))
    print('Done')
except TimeoutException:
    print("Connexion too low or connexion lost...")
    driver.quit()
    sys.exit(1)

@NbCallFunction
def download_img_from_link(string_url_img, **kargs):
    if isinstance(download_img_from_link, NbCallFunction):
        string_path = 'data/pic'+str(download_img_from_link.callNumber)+'.jpg'
    else:
        string_path = 'data/pic_default.jpg'
    
    with open(string_path, 'wb') as file:
        response = requests.get(string_url_img)
        print(response) if (not response.ok) else file.write(response.content)

#==== the while loop idea using the last_height and new_height is from @Artjom B. on Stackoverflow \
#==== i find it quite straightforward and useful ====#
SLEEP_EACH_SCROLL = 5
last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height
count, limit = 0, 10 # if we want to stop
s = set()

while count < limit :
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SLEEP_EACH_SCROLL)
    
    # Retrieve the divs list
    all_divs = driver.find_elements(By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w']")
    selected_divs = [x for x in all_divs if x not in s]
    # Retrieve each image srcset attribute in each div in the divs list
    img_srcset = [div.find_element(By.CSS_SELECTOR, "img").get_attribute('srcset') for div in selected_divs]
    pattern = re.compile('^http\S+')
    # Retrieve the correct image url from image srcset list
    string_url_imgs = [re.match(pattern=pattern, string=x).group() for x in img_srcset]
    for string_url_img in string_url_imgs:
        download_img_from_link(string_url_img)
    
    # Calculate new scroll height and compare with last scroll height 
    # ... (if the scrolling actually changed something)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    count += 1 # count will be used for pagination afterwards
    s = set(all_divs) # Saving this list to avoid downloading again the same photos
    print("scrolling number : " + str(count) + " on limit : " + str(limit))
    #for 73 images i got 465 Ko, so 6.5 Ko in average for each image, 
    #i guess we can go until 200 Mo => 30K photos
