import random, time
from PIL import Image, ImageFilter
import math
import os
import matplotlib.pyplot as plt
import sys
import numpy as np

# make a heightmap from a basic one shaped with a simple image processing tool such as paint
# program usage: give to main the map used as a base, then the folder to save the one generated autocompleted by
# a time identifier. coeff and step passed are additional argument used in the diamond square algortihm.

# to do:
# suppress layer of mountain for better matching (presque fini)
# more realistic mountain (huge work)
# user friendly version with understandable and good default argument (done almost)
# saving in .ben format for unity (ez)
# GUI (???)




count = 0


# bouge le curseur prenant comptre des retour a la ligne etc.
# le cursuer doit etre bien placé a l'origine !
def MoveCurseur(size, curseur, ecart):
    newCurseur = curseur + 2 * ecart
    if curseur // size != newCurseur // size:  # ligne differente !
        newCurseur = ((curseur // size) + 2 * ecart) * size + ecart
    if newCurseur > size * size:
        return -1
    return newCurseur


def MapAnalyser(filename, datah):  # filename of the basic shape !
    img = Image.open(filename)
    size = img.size[0]
    if size != img.size[1]:
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
    datab = list(img.getdata())
    img.close()
    layer = []
    rep = [0 for k in range(256)]
    for k in range(size * size):
        rep[datab[k][0]] += 1
        if (rep[datab[k][0]] == 1):
            layer.append([datab[k][0], datah[k], datah[k]])  # layer, min corresponding, max corrsponding
        else:
            i = 0
            print(layer)
            print(datab[k])
            while (layer[i][0] != datab[k][0]):
                i += 1
            if (layer[i][1] > datah[k]):
                layer[i][1] = datah[k]
            if (layer[i][2] < datah[k]):
                layer[i][2] = datah[k]
    print("{} layer found".format(len(layer)))
    layerOrder = [layer[k][0] for k in range(len(layer))]
    layerOrder.sort()
    layerOrdered = [layer[k] for k in layerOrder]
    for k in range(len(layer)):
        print("layer {} : from {} to {}".format(k + 1, layerOrdered[k][1], layerOrdered[k][2]))
    return layerOrdered


def ElevC(curseurP, ecart, size, mat, coeff):
    som = 0
    div = 0
    if (curseurP - ecart * size > 0):  # audessu
        som += mat[curseurP - ecart * size][0]
        div += 1
    if (curseurP + ecart * size < size * size):  # endessous
        som += mat[curseurP + ecart * size][0]
        div += 1
    if ((curseurP) // size == (curseurP + ecart) // size):  # adroite
        som += mat[curseurP + ecart][0]
        div += 1
    if ((curseurP) // size == (curseurP - ecart) // size):  # agauche
        som += mat[curseurP - ecart][0]
        div += 1
    avg = som // div
    if div != 4:
        global count
        count += 1
    elev = RandRangeNormal(avg - coeff, avg + coeff, ecart)
    if elev > 255:
        elev = 255
    if elev < 0:
        elev = 0
    return elev


def BenFormat(datah, odP, folder):
    bytefile = open(folder + "/map.ben", 'wb')
    hearder = [1, 2, 3]
    datah = [datah[k][0] for k in range(len(datah))]
    bytefile.write(bytes(hearder))
    bytefile.write(bytes([odP]))
    bytefile.write(bytes(datah))
    bytefile.close()


def ApplyDiam1(mat, curseur, ecart, size, coeff, it=0):
    # phase wiki diamant
    avg = (mat[curseur + ecart + ecart * size][0] + mat[curseur - ecart + ecart * size][0] +
           mat[curseur + ecart - ecart * size][0] + mat[curseur - ecart - ecart * size][0]) // 4
    elev = RandRangeNormal(avg - coeff, avg + coeff, ecart)
    if elev > 255:
        elev = 255
    if elev < 0:
        elev = 0
    if ecart != 0:
        mat[curseur] = (elev, elev, elev)
    else:
        mat[curseur] = (elev, 0, 0)
    return mat


def ApplyDiam2(mat, curseur, ecart, size, coeff, it=0):  # applique 1 etape de l'algo
    # phase wiki carré:
    ele = ElevC(curseur + ecart, ecart, size, mat, coeff)
    mat[curseur + ecart] = (ele, ele, ele)
    ele = ElevC(curseur - ecart, ecart, size, mat, coeff)
    mat[curseur - ecart] = (ele, ele, ele)
    ele = ElevC(curseur + ecart * size, ecart, size, mat, coeff)
    mat[curseur + ecart * size] = (ele, ele, ele)
    ele = ElevC(curseur - ecart * size, ecart, size, mat, coeff)
    mat[curseur - ecart * size] = (ele, ele, ele)
    return mat


def ApplyDiamTest(mat, curseur, ecart, size):  # applique 1 etape de l'algo
    # phase wiki diamant
    mat[curseur] = 'd'
    # phase wiki carré:
    # if((curseur + ecart) // size == curseur //size and curseur + ecart < size*size):
    mat[curseur + ecart] = 'c'
    # if ((curseur - ecart) // size == curseur // size and curseur - ecart > 0):
    mat[curseur - ecart] = 'c'
    # if(curseur + ecart*size < size * size):
    mat[curseur + ecart * size] = 'c'
    # if(curseur - ecart*size > 0):
    mat[curseur - ecart * size] = 'c'


def MoveCurseurFilter(size, curseur):
    if (curseur + 3 > size * size):
        return -1
    if (curseur + 3) // size != curseur // size:
        nCurseur = (curseur // size + 3) * size + 1
        if nCurseur > size * size:
            return -1
        return nCurseur
    return curseur + 3


def ImageAnalyzer(im, size, title="default", show=0):  # analyse le contenu de l'image, pas l'image elle meme
    print("analysing ...")
    max = 0
    maxElev = 0
    idMaxRep = 0
    rep = [0 for k in range(256)]
    for k in range(size * size):
        rep[im[k][0]] += 1
        if im[k][0] > maxElev:
            maxElev = im[k][0]
    for k in range(256):
        rep[k] = rep[k] / (size * size) * 100
        if rep[k] > max:
            max = rep[k]
            idMaxRep = rep[k]
    print("results:")
    # for k in range(256):
    #     print("{} : {} %".format(k,rep[k]))
    print("max : {}".format(idMaxRep))
    if show == 1:
        plt.plot(rep)
        plt.title(title)
        plt.show()
    return (idMaxRep, maxElev)


def RandRangeNormal(deb, fin, ecart):
    if ecart == 16:  # at step 6 we take gaussian distribution, thus w'll get a lot of plain but some mountain and valley aswell.
        mu = (fin + deb) / 2
        sig = (fin - mu) / 3
        if sig <= 0:
            print(sig)
            return deb - fin
        return int(np.random.normal(mu, sig))
    return (random.randrange(deb, fin))


def AdaptedFilter(datah, size, folder):
    curseur = size + 1
    while (curseur != -1):
        ecart = 1
        datah[curseur + 1] = datah[curseur]
        datah[curseur - 1] = datah[curseur]
        datah[curseur - size] = datah[curseur]
        datah[curseur - size - 1] = datah[curseur]
        datah[curseur - size + 1] = datah[curseur]
        datah[curseur + size] = datah[curseur]
        datah[curseur + size + 1] = datah[curseur]
        datah[curseur + size - 1] = datah[curseur]
        curseur = MoveCurseurFilter(size, curseur)
    imgOutGauss = Image.new('RGB', (size, size))
    imgOutGauss.putdata(datah)
    imgOutGauss = imgOutGauss.filter(ImageFilter.GaussianBlur(7))
    imgOutGauss.save("{}/allelu{}.png".format(folder, "ownfilter"))
    imgOutGauss.close()


def LinearOnMnt(datah, minEle, maxEle, size, OrigData):
    linearA = (minEle - 255) / (minEle - maxEle)
    linearB = 255 - (linearA * maxEle)
    for i in range(size * size):
        if OrigData[i][0] > 200:
            ele = int(datah[i][0] * linearA + linearB)
            datah[i] = (ele, ele, ele)


def LinearFromAvg(datah, size):
    ir = ImageAnalyzer(datah, size, "Avant", 1)
    avg = ir[0]
    max = ir[1]
    linearA = (avg - 255) / (avg - max)
    linearB = 255 - (linearA * max)
    for i in range(size * size):
        ele = int(datah[i][0] * linearA + linearB)
        datah[i] = (ele, ele, ele)
    ImageAnalyzer(datah, size, "apres", 1)


def polynomial(datah, size):
    ir = ImageAnalyzer(datah, size)
    avg = ir[0] + 60
    max = ir[1]
    if avg >= max:
        avg = max - 10;
    B = (255 + max * max / (avg)) / (max * max / avg + max)
    A = (B * avg - avg) / (avg * avg)
    print("equ: {} x2 + {} x".format(A, B))
    for i in range(size * size):
        ele = int(A * datah[i][0] * datah[i][0] + B * datah[i][0])
        if ele > 255:
            ele = 255
        if ele < 1:
            ele = 1
        datah[i] = (ele, ele, ele)
        # ImageAnalyzer(datah,size,"apres",1)


def TheMountains(datah, OrigData, size, filter, filterName,folder):  # meme que filtre et sauvegarde mais avec le coeff des montagnes
    minEle = 255
    maxEle = 1
    mtArea = 0
    imgOut = Image.new('RGB', (size, size))
    imgOut.putdata(datah)
    imgOut = imgOut.filter(filter)
    datah = list(imgOut.getdata())
    # ImageAnalyzer(datah,size)
    for i in range(size * size):
        if OrigData[i][0] > 200:
            if minEle > datah[i][0]:
                minEle = datah[i][0]
            if maxEle < datah[i][0]:
                maxEle = datah[i][0]
            mtArea += 1
    print("mountain area : {} pixel ({}%)".format(mtArea, mtArea / (size * size) * 100))
    print("mountain area : min Elev:{} max Elev:{})".format(minEle, maxEle))
    print("starting reelevation process")
    # LinearOnMnt(datah,minEle,maxEle,size,OrigData)
    # LinearFromAvg(datah,size)
    polynomial(datah, size)
    # ImageAnalyzer(datah,size)
    imgOut.putdata(datah)
    imgOut.save("{}/allelu{}{}".format(folder, filterName, 'Mountained.png'))
    imgOut.close()


def FilterAndSave(datah, size, filter, filterName, folder):
    imgOutGauss = Image.new('RGB', (size, size))
    imgOutGauss.putdata(datah)
    imgOutGauss = imgOutGauss.filter(filter)
    imgOutGauss.save("{}/allelu{}.png".format(folder, filterName))
    imgOutGauss.close()


def CreteGen():
    return 0


def FindContour(dataOrig, i):
    return 0


def MountainFinder(dataOrig, size):
    Mountain = []
    for i in range(size * size):
        if (dataOrig[i][0] == 255):
            Mountain += [FindContour(dataOrig, i)]

    return 0


def main(filename, folder, coeff, StepPassed):
    Ts = time.localtime()
    folder = folder.format(Ts.tm_min, Ts.tm_sec)
    if not os.path.exists(folder):
        print("creating new folder in {}".format(folder))
        os.makedirs(folder)
    else:
        print("erreur !")
        return 0

    nxtCoeff = 0
    while (nxtCoeff < len(coeff)):
        CurrCoeff = coeff[nxtCoeff]
        FolderCoeff = folder + "/" + coeff[nxtCoeff + 1]
        os.makedirs(FolderCoeff)
        print("{} is in {}".format(coeff[nxtCoeff + 1], FolderCoeff))
        img = Image.open(filename)
        size = img.size[0]
        if size != img.size[1]:
            print("Error : Image is not square !")
        odP = 0
        for k in range(0, 500):
            if math.pow(2, k) + 1 == size:
                odP = k
                break

        if (odP == 0):
            print("Square dimension must be 2^n+1")
            return 0

        print("size : {} = 2^{} + 1".format(size, odP))
        print("retrieving pixels ...")
        datah = list(img.getdata())
        Original = [k for k in datah]
        img.close()
        # data = [datah[k][0] for k in range(0, len(datah))]
        curseur = size * size // 2
        ecart = size // 2
        inc = 0
        for k in range(StepPassed):
            ecart = ecart // 2
            curseur = ecart + ecart * size
            inc += 1
        while (ecart != 0):
            print("step {} out of {} : ecart {} coeff {}".format(inc, odP, ecart, CurrCoeff[inc]))
            curseurP = curseur
            while (curseur != -1):
                datah = ApplyDiam1(datah, curseur, ecart, size, CurrCoeff[inc])
                curseur = MoveCurseur(size, curseur, ecart)
            curseur = curseurP
            while (curseur != -1):
                datah = ApplyDiam2(datah, curseur, ecart, size, CurrCoeff[inc])
                curseur = MoveCurseur(size, curseur, ecart)
            ecart = ecart // 2
            curseur = ecart + ecart * size
            inc += 1
            # im = [(data[i],data[i],data[i]) for i in range(size*size)]
            imgOut = Image.new('RGB', (size, size))
            imgOut.putdata(datah)
            imgOut.filter(ImageFilter.GaussianBlur(20))
            imgOut.save("{}/alleluTestCoeff{}.png".format(FolderCoeff, inc))
            imgOut.close()
        print("repacking...")
        FilterAndSave(datah, size, ImageFilter.GaussianBlur(3), "Gauss", FolderCoeff)
        TheMountains(datah, Original, size, ImageFilter.GaussianBlur(3), "GaussMountain", FolderCoeff)
        print("HMs created in {}".format(FolderCoeff))
        nxtCoeff += 2
        BenFormat(datah, odP, FolderCoeff)
    print(count)


coeff = [[10, 10, 10, 10, 10, 10, 25, 10, 10, 8, 4], "25101084"]
main("C:/Users/BEN/Pictures/ARDA_Project/hm1.png", "C:/Users/BEN/Pictures/ARDA_Project/test{}{}", coeff, 5)


def Test():
    list = ['-' for k in range(289)] #['-']*289

    print("phase 1")
    nc = 144
    while (nc != -1):
        ApplyDiamTest(list, nc, 8, 17)
        nc = MoveCurseur(17, nc, 8)

    for k in range(17):
        for g in range(17):
            print(list[k * 17 + g], end=' ')
        print(" ")

    print("phase 2")
    nc = 72
    while (nc != -1):
        ApplyDiamTest(list, nc, 4, 17)
        nc = MoveCurseur(17, nc, 4)

    for k in range(17):
        for g in range(17):
            print(list[k * 17 + g], end=' ')
        print(" ")

    print("phase 3")
    nc = 36
    while (nc != -1):
        ApplyDiamTest(list, nc, 2, 17)
        nc = MoveCurseur(17, nc, 2)

    for k in range(17):
        for g in range(17):
            print(list[k * 17 + g], end=' ')
        print(" ")

    print("phase 4")
    nc = 18
    while (nc != -1):
        ApplyDiamTest(list, nc, 1, 17)
        nc = MoveCurseur(17, nc, 1)

    for k in range(17):
        for g in range(17):
            print(list[k * 17 + g], end=' ')
        print(" ")

    print("---------------5------------------")
    list = ['-' for k in range(25)]

    print("phase 1")
    nc = 12
    while (nc != -1):
        ApplyDiamTest(list, nc, 2, 5)
        nc = MoveCurseur(5, nc, 2)

    for k in range(5):
        for g in range(5):
            print(list[k * 5 + g], end=' ')
        print(" ")

    print("phase 2")
    nc = 6
    while (nc != -1):
        ApplyDiamTest(list, nc, 1, 5)
        nc = MoveCurseur(5, nc, 1)

    for k in range(5):
        for g in range(5):
            print(list[k * 5 + g], end=' ')
        print(" ")


print("done")
# Test()
