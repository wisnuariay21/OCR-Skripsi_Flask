from PIL import Image
import pytesseract
from gtts import gTTS
import cv2 
import numpy as np
from skimage.filters import (threshold_sauvola)

def applythresh(filename):
    imgfile = np.float32(filename)
    noise = cv2.medianBlur(imgfile,5).astype('uint8')
    thresh_sauvola = threshold_sauvola(noise, window_size=25)
    sauvola = noise > thresh_sauvola
    sauvola = sauvola.astype(np.uint8)
    sauvola*=255
    return sauvola

def openfile(filename):
    file = Image.open(filename)
    return file

def grayscale(filename):
    return cv2.cvtColor(filename, cv2.COLOR_BGR2GRAY)

def imgstring(filename):
    text = pytesseract.image_to_string(filename)
    return text

def textspeech(filename):
    text = gTTS(text=filename, lang='id', slow=False)
    return text

