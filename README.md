# Training artificial neural network to recognize selfies from autoportraits 

```diff
- This work is in progress. Also I'm still a student so if you'd like to share any feedbacks or to correct me in some point, please do so ! That will always be much appreciated ! 
```

## Introduction

I'm going to use Instagram social network alongside Python 3.0+ with Selenium package for supervised learning classification purposes.

I'm going to use Selenium as [Facebook deprecated Instagram API Platform](https://www.instagram.com/developer/), and its new Instagram Graph API is a bit tricky to use with 'sandbox' muddle.

## Methods

Following the hasthag #faceportrait and #selfies, I am going to scrape a certain amount of photos (still to be decided) separately looking for people's selfies and self-portraits, so that I'll train my algorithm recognizing which photo is a selfie, and which one is a self-portrait.

Distinction between selfies and self-portraits is based on the definition of the former : "A selfie is a self-portrait photograph taken with a **hand-held** digital camera or camera phone".


## How to use it 
* *Selfie_Instagram.py* retrieve images from Instagram
- It takes as console arguments as much as hashtags names as you want
- It ends with a boolean : True if the file needs to be save as selfie or False if it's not.

Example :

```
## Runnning the script looking for #faceportrait #notselfie and save it as notselfie
python Selfie_Instagram.py faceportrait notselfie False
```

* *CleaningPhotos.py* clean saved images
- It takes as console arguments a boolean to define whether it is a Selfie or not

Here is a Selfie_Instagram.py working demo:
![demo](./img/demo.gif)

## Results

From the scrapping part only, here is a demo of what we can expect so far. 
You will find more detailed explanations inside python files itself.


* Expected data before cleaning : 
![demo](./img/unfiltered_data)

* After Cleaning :
![demo](./img/unfiltered_data)
