import random, time
from PIL import Image, ImageFilter
import math

#sort plusieur version moyenner

def main(filename):
    ## ouverture et verification

    basemode = Image.open(filename)
    for i in range(1):
        blurred = basemode.filter(ImageFilter.GaussianBlur(25))
        blurred.save("C:/Users/BEN/Pictures/ARDA_Project/blurredbob3.png")





main("C:/Users/BEN/Pictures/ARDA_Project/hm1.png")