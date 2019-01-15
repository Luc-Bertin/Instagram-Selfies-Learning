from decorators import *
import sys
import os, os.path

DIR = './data/'

## Filtering photos ##
if (sys.argv[-1]=="True" or sys.argv[-1]=="False"):
    Boolean = eval(sys.argv[-1])
else:
    raise TypeError("Last Argument needs to be a Boolean")


## Cleaning and filtering images
if Boolean==False:
    ## number of files in /data starting with 'selfie'
    x = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and name.startswith('notselfie')])
    for i in range(1,x):
        img_path = 'data/notselfie'+str(i)+'.jpg'
        face_finder(img_path)
else:
    ## number of files in /data starting with 'notselfie'
    x = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and name.startswith('selfie')])
    for i in range(1,x):
        img_path = 'data/selfie'+str(i)+'.jpg'
        face_finder(img_path)