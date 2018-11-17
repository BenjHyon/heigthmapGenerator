import random, time
from PIL import Image, ImageFilter
import math


def carrediamant(t, h, base,rate):
    t[0][0] = base[0]
    t[0][h-1]=base[h*(h-1)]
    t[h-1][0]=base[h-1]
    t[h-1][h-1]=base[h-1+ (h-1) * h]





def maxVal(t):
    maxV = []
    for x in range(len(t)):
        maxV += [max(t[x][:])]
    return max(maxV)


def minVal(t):
    maxV = []
    for x in range(len(t)):
        maxV += [min(t[x][:])]
    return min(maxV)

def greyscalepng(b):
    t = b[:]
    scale = len(t)
    coeff = 255 / (maxVal(t) - minVal(t))
    for x in range(0, scale):
            for y in range(0, scale):
                t[x][y] = int(coeff * t[x][y])

    ##adaptation au format RGB de PILLOW
    im = [0 for i in range(len(t) * len(t))]
    imgOut = Image.new('RGB', (scale, scale))
    for x in range(scale):
        for y in range(scale):
            im[x + y * scale] = (t[x][y], t[x][y], t[x][y])
    imgOut.putdata(im)
    imgOut.show()
    #exit = input()

def main(filename, nbHmgenere):
    ## ouverture et verification

    basemode = Image.open(filename)
    scale = basemode.size[0]
    if scale != basemode.size[1]:
        print("Erreur ! l'image fourni n'est pas carré :")
    puissanceenieme = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == scale:
            puissanceenieme = 1
            break
    if (puissanceenieme == 0):
        print("les dimensions du carrée ne sont pas bonnes, veuillez selectionner une autre ebauche")
        return 0

    print("Moyennage de l'ebauche")
    #blurred = basemode.filter(ImageFilter.GaussianBlur(30))
    # blurred.save('E:/projet2A/MAP2018modGB2.png')
    print("...done\n")
    print("création du tableau de la variabilité")
    datah = list(basemode.getdata())
    data = [datah[k][0] for k in range(0, len(datah))]
    datal = [data[k] for k in range(len(data))] #ajouter un coefficient
    print("...done\n")
    for k in range(0, nbHmgenere):
        print("creating heightmap n{} of {}".format(k + 1, nbHmgenere))

        t = [[0 for i in range(scale)] for k in range(scale)]

        carrediamant(t, scale, datal)############################################ICI

        offset = -minVal(t)
        for x in range(0, scale):
            for y in range(0, scale):
                t[x][y] = offset + t[x][y]
        coeff = 255 / (maxVal(t) - minVal(t))

        # coeff pour matché avec le format RGB
        for x in range(0, scale):
            for y in range(0, scale):
                t[x][y] = int(coeff * t[x][y])

        ##adaptation au format RGB de PILLOW
        im = [0 for i in range(len(t) * len(t))]
        imgOut = Image.new('RGB', (scale, scale))
        for x in range(scale):
            for y in range(scale):
                im[x + y * scale] = (t[x][y], t[x][y], t[x][y])
        imgOut.putdata(im)

        imtext = [0 for i in range(len(t) * len(t))]
        imgOuttext = Image.new('RGB', (scale, scale))
        water = 75

        grass = 190
        grass_tmax = 220
        grass_tmin = 195

        ga = (grass_tmin - grass_tmax)/(grass-1-water)
        gb = ga * water + grass_tmax

        dirt = 225
        dirtRmax = 130
        dirtRmin = 90
        dirtGmax = 70
        dirtGmin = 40

        Ra = (dirtRmin - dirtRmax)/(dirt-1-grass)
        Ga = (dirtGmin - dirtGmax)/(dirt-1-grass)

        Rb = -Ra * grass + dirtRmax
        Gb = -Ga * grass + dirtGmax
        print("creation de la map texturé")
        Ts = time.localtime()
        for x in range(scale):
            for y in range(scale):
                if (t[x][y] < water):##water
                    imtext[x + y * scale] = (0,int(125 *(0.5+t[x][y]/75*0.5)), int(255 *(0.5+t[x][y]/75*0.5)))
                elif (t[x][y] < grass): ## grass
                    imtext[x + y * scale] = (0,int(ga*t[x][y]+gb),0)
                elif (t[x][y] < dirt): ## dirt
                    imtext[x + y * scale] = (int(Ra*t[x][y]+Rb),int(Ga*t[x][y]+Gb),0)
                else:
                    imtext[x + y * scale] = (255,255,255)
        imgOuttext.putdata(imtext)
        imgOuttext.save('E:/projet2A/testhm/texturemap{}{}.png'.format(Ts.tm_min,Ts.tm_sec))

        ## création du fichier

        ## with pillow:
        imgOut.save('E:/projet2A/testhm/heightmap{}{}.png'.format(Ts.tm_min,Ts.tm_sec))



main("E:/projet2A/map5.png",1)
