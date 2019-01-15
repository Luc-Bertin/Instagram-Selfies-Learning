from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
import cv2
import os

class NbCallFunction:
    def __init__(self, function):
        self.callNumber = 0
        self.function = function
    def __call__(self, *args, **kwargs):
        ## onCall
        self.callNumber += 1
        return self.function(*args, **kwargs)

class Navigation:
    
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, elementTupleInfos, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(elementTupleInfos))
        ## Handling TimeOutException if connection is bad or even nonxistent
        except TimeoutException:
            print("Timed out waiting for " +str(elementTupleInfos)+ "tuple to load.")
            driver.quit()
            sys.exit(1)

    def click_if_exists(self, elementTupleInfos):
        try:
            self.driver.find_element(elementTupleInfos[0], elementTupleInfos[1]).click()
        except NoSuchElementException:
            print("Actually, there was nothing to be clicked on.")


@NbCallFunction
def download_img_from_link(string_url_img, selfie_or_not, **kargs):
    if isinstance(download_img_from_link, NbCallFunction):
        if selfie_or_not==False:
            string_path = 'data/notselfie'+str(download_img_from_link.callNumber)+'.jpg'
        else:
            string_path = 'data/selfie'+str(download_img_from_link.callNumber)+'.jpg'
    else:
        string_path = 'data/notselfie_default.jpg'

    with open(string_path, 'wb') as file:
        response = requests.get(string_url_img)
        print(response) if (not response.ok) else file.write(response.content)


def face_finder(img_path):
    faceCascade =  cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    ## initalize parameters
    maxArea = 0
    x = 0
    y = 0
    w = 0
    h = 0
    rectangleColor = (0,255,0)
    try:
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=0)
        ## Loop over all faces and check if the area for this face is the largest so far
        
        for (_x,_y,_w,_h) in faces:
            if  _w*_h > maxArea:
                x = _x
                y = _y
                w = _w
                h = _h
                maxArea = w*h
        ## if the maxArea of detected face is bigger than 35% of the original photo then keep it
        print(maxArea)
        if maxArea > 0.15*150*150:
            #cv2.rectangle(gray, (x, y), (x+w, y+h), rectangleColor, 2)
            cv2.imwrite(img_path, gray)
        else:
            os.remove(img_path)
        #cv2.imshow("new-image", gray)
        #cv2.waitKey(0)
    except:
        print('A problem occured while opening the image or trying to find a face')
