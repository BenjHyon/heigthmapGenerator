import random, time
from PIL import Image, ImageFilter
import math
import os
import matplotlib.pyplot as plt
import sys
import numpy as np

#Make a realistic HeightMap of a mountain from the shape of a mountain from it's png value
#Known Issue: Little shape with 1 pixel wide area is not well defined

#to do:

count = 0

########SHAPER
#1 8 7
#2 x 6
#3 4 5
def GetTheIndex8(datah,current):
    edges = {}
    #Check if we are at the edge:
    for k in range(8):
        edges[k] = GetIndexFromCursorAndRelativPos(datah,current,k)
    return edges

def GetIndexFromCursorAndRelativPos(datah,cursor,RelativPos, radius = 1):
    size = math.sqrt(len(datah))
    sizeM = size * size
    if(size != int(size)):
        raise ValueError('map is not square !')
    size = int(size)
    if RelativPos == 0:
        if cursor - size*radius-radius > 0:
            return cursor - size * radius-radius
        return -1
    if RelativPos == 1:
        if cursor - radius > 0:
            return cursor - radius
        return -1
    if RelativPos == 2:
        if cursor + size*radius -radius < sizeM:
            return cursor + size*radius - radius
        return -1
    if RelativPos == 3:
        if cursor + size*radius < sizeM:
            return cursor + size*radius
        return -1
    if RelativPos == 4:
        if cursor + size*radius + radius < sizeM:
            return cursor + size*radius + radius
        return -1
    if RelativPos == 5:
        if cursor + radius < sizeM:
            return cursor + radius
        return -1
    if RelativPos == 6:
        if cursor - size*radius + radius > 0:
            return cursor - size*radius + radius
        return -1
    if RelativPos == 7:
        if cursor - size*radius > 0:
            return cursor - size*radius
        return -1
    raise ValueError('trying to acces to relative position {} but only 0 to 7 is supported'.format(RelativPos))

def FindNext(datah,elevM,current,prec = -1):
    if prec == -1:#debut
        indexOfAjdacent = GetTheIndex8(datah,current)
        diff = [0]*8
        for k in range(7):
            if indexOfAjdacent[k] != -1 and indexOfAjdacent[k+1] != -1:
                diff[k] = abs(datah[indexOfAjdacent[k]]-datah[indexOfAjdacent[k+1]])
        if indexOfAjdacent[7] != -1 and indexOfAjdacent[0] != -1:
            diff[7]=abs(datah[indexOfAjdacent[7]]-datah[indexOfAjdacent[0]])
        maxInd = diff.index(max(diff))#now i have to decide which index to take between 2
        if maxInd == 7:
            if datah[indexOfAjdacent[0]] == elevM:
                return indexOfAjdacent[0]
            elif datah[indexOfAjdacent[7]] == elevM:
                return indexOfAjdacent[7]
            else:
                return current #when returning current we know we are on a lonely mountain
    indexOfAjdacent = GetTheIndex8(datah,current)
    diff = [0]*8
    for k in range(7):
        if indexOfAjdacent[k] != -1 and indexOfAjdacent[k+1] != -1 and indexOfAjdacent[k] != prec and indexOfAjdacent[k+1] != prec:
            diff[k] = abs(datah[indexOfAjdacent[k]]-datah[indexOfAjdacent[k+1]])
    if indexOfAjdacent[7] != -1 and indexOfAjdacent[0] != -1:
        diff[7]=abs(datah[indexOfAjdacent[7]]-datah[indexOfAjdacent[0]])
    maxInd = diff.index(max(diff))#now i have to decide which index to take between 2
    if maxInd == 7:
        if datah[indexOfAjdacent[0]] == elevM:
            return indexOfAjdacent[0]
        elif datah[indexOfAjdacent[7]] == elevM:
            return indexOfAjdacent[7]
        else:
            return current #when returning current we know we are on a lonely mountain
    if datah[indexOfAjdacent[maxInd]] == elevM:
        return indexOfAjdacent[maxInd]
    elif datah[indexOfAjdacent[maxInd +1]] == elevM:
        return indexOfAjdacent[maxInd +1]
    else: return current

def loadImage(filename):
    img = Image.open(filename)
    size = img.size[0]
    if size != img.size[1]:
        print("Error : Image is not square !")
    return [k[0] for k in list(img.getdata())]

def saveImage(datah,folder,name = 'default'):
    size = math.sqrt(len(datah))
    size = int(size)
    img = Image.new('RGB',(size,size))
    datak = [(a,b,c) for a,b,c in datah]
    img.putdata(datak)
    img.save(folder+"/ARDAP_{}.png".format(name))


def GetFirstPixelOfMountain(datah,elevM):
    for k in range(len(datah)):
        if datah[k] == elevM:
            return k
    raise ValueError('specified elevation is not found in that sample')

def MountainShape(datah, elevM, startingP):
    maxValue = 255 #255 for png, could be set to 511 if 2bytes format is supported
    mntShape = []
    debugRcolor = random.randrange(0,255)
    debugGcolor = random.randrange(0,255)
    debugBcolor = random.randrange(0,255)
    if datah[startingP] != elevM:
        raise ValueError('startingPoint is not set on good elevation : given {} expected {}'.format(datah[startingP],elevM))
    if elevM< 0 or elevM > maxValue:
        raise ValueError('Mountain level is set to unsupported elevation, must be between 0 and {}, gien {}'.format(maxValue,elevM))
    dataDebug = [[k,k,k] for k in datah]
    prec = startingP
    current = FindNext(datah,elevM,prec)
    mntShape +=[current]
    step = 1
    dataDebug[startingP][1]=255
    dataDebug[current][0]=255
    global count
    while(current != startingP):
        new = FindNext(datah,elevM,current,prec)
        prec = current
        current = new
        mntShape +=[current]
        if current == prec:#step back
            current = prec
            prec = new
        step += 1
        # save here for debug:
        dataDebug[current] = [debugRcolor,debugGcolor,debugBcolor]
    saveImage(dataDebug,"C:/Users/BEN/Pictures/ARDA_Project/Debug","step{}".format(count))
    return mntShape

########FRACTALISER



def Average(datah,elevM,startingP):
    size = int(math.sqrt(len(datah)))
    datak = [k for k in datah]
    mntShape = MountainShape(datak,elevM,startingP)
    RightestColomn = 0
    posInLineMin = size
    posInLineMax = 0
    for k in range(len(mntShape)):
        posInLine = mntShape[k]%size
        if posInLineMin > posInLine:
            posInLineMin = posInLine
        if posInLineMax < posInLine:
            posInLineMax = posInLine
    posInColMin = size
    posInColMax = 0
    for k in range(len(mntShape)):
        posInCol = mntShape[k]//size
        if posInColMin > posInCol:
            posInColMin = posInCol
        if posInColMax < posInCol:
            posInColMax = posInCol
    # dataIm = [[a,a,a] for a in datah]
    # dataIm[posInLineMin + size * posInColMin] = [255,255,255]
    # dataIm[posInLineMax + size * posInColMin] = [255,255,255]
    # dataIm[posInLineMin + size * posInColMax] = [255,255,255]
    # dataIm[posInLineMax + size * posInColMax] = [255,255,255]
    # saveImage(dataIm,"C:/Users/BEN/Pictures/ARDA_Project/Debug")



#######Main
Average(loadImage("C:/Users/BEN/Pictures/ARDA_Project/MntPOC2.png"),195,GetFirstPixelOfMountain(loadImage("C:/Users/BEN/Pictures/ARDA_Project/MntPOC2.png"),195))

#Get the shape of the mountain  v
#draw fractale line  x
#randomnize fractale height  x
#get down to the valley  x

#sample of code that don't work yet:
    # for k in range(len(mntShape)):
    #     datak[mntShape[k]] = 75
    # while(1 == 1):
    #     indexNeighboors = GetTheIndex8(datak,startingP)
    #     for k in range(7):
    #         if datak[indexNeighboors[k]] == elevM and indexNeighboors[k] != -1:
    #             nStartingP = indexNeighboors[k]
    #             nStartingPvalue = datak[nStartingP]
    #     if nStartingP == startingP:
    #         print("done")
    #         return 0
    #     startingP = nStartingP
    #     mntShape = MountainShape(datak,elevM,nStartingP)
    #     for k in range(len(mntShape)):
    #         datak[mntShape[k]] = 75