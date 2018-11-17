import sys
from PIL import Image
import math

def Formater(folder,filename):

    f = open(folder+filename, "rb")
    header = f.read(3)
    if(int(header[0]) == 1 and int(header[1]) == 2 and int(header[2]) == 3):
        print("Good Format")
    size = int(math.pow(2,int(f.read(1)[0]))+1)
    print("size: {}".format(size))
    datah = [(0,0,0) for k in range(size*size)]
    for k in range(size * size):
        px = int(f.read(1)[0])
        datah[k] = (px,px,px)
    imgOut = Image.new('RGB', (size, size))
    imgOut.putdata(datah)
    imgOut.save("{}/Reformated.png".format(folder))
    imgOut.close()
    f.close()


Formater("C:/Users/BEN/Pictures/ARDA_Project/","map.ben")