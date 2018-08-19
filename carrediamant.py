import random, time
from PIL import Image, ImageFilter
import math


def carrediamant(t, h,):
    t[0][0] = 0#random.randrange(-h, h)
    t[0][h - 1] =0 # random.randrange(-h, h)
    t[h - 1][0] =0 #random.randrange(-h, h)
    t[h - 1][h - 1] =0 #random.randrange(-h, h)
    i = h - 1
    fordt = 0
    while (i > 1):
        id = i // 2
        for x in range(id, h, i):##diamant
            fordt+=1
            for y in range(id, h, i):
                average = (t[x - id][y - id] + t[x - id][y + id] + t[x + id][y + id] + t[x + id][y - id]) / 4
                t[x][y] = average + random.randrange(-id, id)

        for x in range(0, h, id):##carre
            if x % i == 0:
                shift = id
            else:
                shift = 0
            for y in range(shift, h, i):
                summ = 0
                n = 0
                if x >= id:
                    summ += t[x - id][y]
                    n += 1
                if x + id < h:
                    summ += t[x + id][y]
                    n += 1
                if y >= id:
                    summ += t[x][y - id]
                    n += 1
                if y + id < h:
                    summ += t[x][y + id]
                    n += 1
                t[x][y] = summ / n + random.randint(-id, id) ## base [x +y * h]
        i = id


def maxVal(t):
    maxV = []
    for x in range(len(t)):
        maxV += [max(t[x][:])]
    return max(maxV)


def minVal(t):
    minV = []
    for x in range(len(t)):
        minV += [min(t[x][:])]
    return min(minV)



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
    blurred = basemode.filter(ImageFilter.GaussianBlur(75))
    # blurred.save('E:/projet2A/MAP2018modGB2.png')
    print("...done\n")
    print("création du tableau de la variabilité")
    datah = list(blurred.getdata())
    data = [datah[k][0] for k in range(0, len(datah))]
    datal = [data[k] for k in range(len(data))] #ajouter un coefficient
    print("...done\n")
    for k in range(0, nbHmgenere):
        print("creating heightmap n{} of {}".format(k + 1, nbHmgenere))

        t = [[0 for i in range(scale)] for k in range(scale)]

        carrediamant(t, scale)
        print("carre diamant terminé, traitement ...")
        offset = -minVal(t)
        for x in range(0, scale):
            for y in range(0, scale):
                t[x][y] = offset + t[x][y]
        coeff = 255 / (maxVal(t) - minVal(t))

        ################################################t devient un tableau de valeur [0,255]
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

        ## cst des textures
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


        print("creation de la map texturé non mixé")

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



        ## creation de la map mixé
        #creation des valeur gs
        ratio = 0.75
        immixed = [0 for i in range(scale*scale)]
        for x in range(scale):
            for y in range(scale):
                immixed[x + scale * y] = ratio * t[x][y] + (1-ratio)*data[x + scale * y]

        # au format png [0,255]
        coeff = 255 / (max(immixed) - min(immixed))
        for x in range(0, len(immixed)):
            immixed[x] = int(coeff * immixed[x])
        #mise sous forme de heightmap

        print("creation de la hm mixé")
        imgOutmixed = Image.new('RGB', (scale, scale))
        imhmmixed = [0 for i in range(len(t) * len(t))]
        for x in range(scale):
            for y in range(scale):
                imhmmixed[x + y * scale] = (immixed[x + scale * y], immixed[x + scale * y], immixed[x + scale * y])
        imgOutmixed.putdata(imhmmixed)


        #mise sous forme de map texturé

        print("creation de la map mixé texturé")
        immixedtext = [0 for i in range(len(t) * len(t))]
        imgmixedOuttext = Image.new('RGB', (scale, scale))
        for x in range(scale):
            for y in range(scale):
                if (immixed[x + scale * y] < water):##water
                    immixedtext[x + y * scale] = (0,int(125 *(0.5+immixed[x + scale * y]/75*0.5)), int(255 *(0.5+immixed[x + scale * y]/75*0.5)))
                elif (immixed[x + scale * y] < grass): ## grass
                    immixedtext[x + y * scale] = (0,int(ga*immixed[x + scale * y]+gb),0)
                elif (immixed[x + scale * y] < dirt): ## dirt
                    immixedtext[x + y * scale] = (int(Ra*immixed[x + scale * y]+Rb),int(Ga*immixed[x + scale * y]+Gb),0)
                else:
                    imtext[x + y * scale] = (255,255,255)
        imgmixedOuttext.putdata(immixedtext)

        ##save des images
        Ts = time.localtime()
        imgOutmixed.save('E:/projet2A/testhm/heightmixedmap{}{}.png'.format(Ts.tm_min,Ts.tm_sec))
        imgOut.save('E:/projet2A/testhm/heightmap{}{}.png'.format(Ts.tm_min,Ts.tm_sec))
        imgOuttext.save('E:/projet2A/testhm/texturemap{}{}.png'.format(Ts.tm_min,Ts.tm_sec))
        imgmixedOuttext.save('E:/projet2A/testhm/texturemapmixed{}{}.png'.format(Ts.tm_min,Ts.tm_sec))

main("E:/projet2A/MAP2018.png",1)
