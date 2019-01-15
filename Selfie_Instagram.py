from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

import regex as re
import getpass
import requests
import os
import sys
import time

import credentials
from decorators import *

if len(sys.argv) < 2:
    raise EnvironmentError("not enough arguments passed in")

HASHTAGS = ['#'+str(x) for x in sys.argv][1:-1]
if (sys.argv[-1]=="True" or sys.argv[-1]=="False"):
    Boolean = eval(sys.argv[-1]) 
else:
    raise TypeError("Last Argument needs to be a Boolean")
#HASHTAGS = ["#faceportrait", "#notselfie"]
print(HASHTAGS)

## Options for the web driver (here incognito mode for Chrome, optional)
options = webdriver.ChromeOptions()
options.add_argument(' — incognito')
## Get the webdriver from its location path
driver = webdriver.Chrome(executable_path='/Users/lucbertin/Desktop/chromedriver', options = options)
## Define a callable functino which waits element to load
WaitLoads = Navigation(driver=driver)
## Go to Instagram main connection page
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
WaitLoads(elementTupleInfos=(By.TAG_NAME, 'input'), timeout=10)

## Enter ID/password
driver.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys(credentials.USER_ID)
driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(credentials.USER_PASSWORD)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

## Handle this fucking pop-up while opening Instagram
WaitLoads(elementTupleInfos=(By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']"), timeout=10)
WaitLoads.click_if_exists((By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']"))

for hashtag in HASHTAGS:
    search_bar = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Rechercher']")
    search_bar.send_keys(hashtag)
    time.sleep(3)
    search_bar.send_keys(Keys.ENTER)
    search_bar.send_keys(Keys.ENTER)
    ## All photos that appeared or will appear are located in div[class='v1Nh3 kIKUG  _bz0w']
    WaitLoads(elementTupleInfos=(By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w']"), timeout=10)
    
    ##==== the while loop idea using the last_height and new_height is from @Artjom B. on Stackoverflow \
    ##==== i find it quite straightforward and useful ====##
    SLEEP_EACH_SCROLL = 3
    last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height
    count, limit = 0, 2 # if we want to stop
    s = set()
    
    while True:
        ## Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_EACH_SCROLL)
        
        ## Retrieve the divs list
        all_divs = driver.find_elements(By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w']")
        selected_divs = [x for x in all_divs if x not in s]
        ## Retrieve each image srcset attribute in each div in the divs list
        img_srcset = [div.find_element(By.CSS_SELECTOR, "img").get_attribute('srcset') for div in selected_divs]
        pattern = re.compile('^http\S+')
        ## Retrieve the correct image url from image srcset list
        string_url_imgs = [re.match(pattern=pattern, string=x).group() for x in img_srcset]
    
        for string_url_img in string_url_imgs:
            download_img_from_link(string_url_img, selfie_or_not=Boolean)
        
        ## Calculate new scroll height and compare with last scroll height 
        ## ... (if the scrolling actually changed something)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        count += 1 # count will be used for pagination afterwards
        
        s = set(all_divs) # Saving this list to avoid downloading again the same photos
        print("scrolling number : " + str(count) + " on limit : " + str(limit))
        print("number of photos downloaded : " + str(download_img_from_link.callNumber))
        if download_img_from_link.callNumber > 10000:
            break

"""
29 images for 90 images basically => 1/3 of the photos are wiped out
30K images => 100k photos
For 1 image i got 8.2 Ko,
I guess we can go until 200 Mo => 30K photos
"""
