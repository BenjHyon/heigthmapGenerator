from PIL import Image, ImageFilter
import math

def MaximumsIndex(nbOfMax,tablea):
    MaxI = [nbOfMax for k in range(nbOfMax)]
    for k in range(len(tablea)):
        for i in range(nbOfMax):
            if tablea[k] >= tablea[MaxI[i]]:
                for j in range(nbOfMax-1,i,-1):
                    MaxI[j]= MaxI[j-1]
                MaxI[i] = k
                break
    return MaxI

def NearestValue(value,availValueList):
    ecart = [value-k for k in availValueList]
    return ecart.index(min(ecart))



def Layerer(filename,layerWtd):
    Img = Image.open(filename)
    size = Img.size[0]
    if size != Img.size[1]:
        print("Error : Image to analyse is not square !")
        return -1
    OdP = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == size:
            OdP = k
            break
    if (OdP == 0):
        print("Square dimension must be 2^n+1")
        return -1
    datah = list(Img.getdata())
    Img.close()
    HstG = [0 for k in range (256)]
    for k in range(size*size):
        HstG[datah[k][0]]+=1
    print(HstG)
    value = MaximumsIndex(layerWtd,HstG)
    # for k in range (len(value)-1):
    #     if value[k]==value[k+1]:
    #         print("one or more layer are the same ! layer decresed by 1")
    #         layerWtd -=1
    #         k-=1
    #         value.pop(k)
    print("we have found {} different layer which are : ".format(layerWtd))
    for k in range(len(value)):
        print("Layer {} : {}".format(k+1,value[k]))
    #now set remaining parasite to normal:
    for k in range(size * size):
        if datah[k][0] not in value:
            nearestV = NearestValue(datah[k][0],value)
            datah[k] =(value[nearestV],value[nearestV],value[nearestV])






def MapAnalyser(filename):
    Img = Image.open(filename)
    size = Img.size[0]
    if size != Img.size[1]:
        print("Error : Image to analyse is not square !")
        return -1
    OdP = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == size:
            OdP = k
            break
    if (OdP == 0):
        print("Square dimension must be 2^n+1")
        return -1
    datah = list(Img.getdata())
    Img.close()
    layer = []
    rep = [0]*256


Layerer("C:/Users/BEN/Pictures/ARDA_Project/hm1.png",3)
#print(MaximumsIndex(3,[8,5,0,0,0,0,0,6]))