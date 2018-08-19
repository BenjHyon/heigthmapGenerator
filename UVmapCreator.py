from PIL import Image
import math

#create a basic UV map for heightmap of size 2^n+1

def UV(folder,filename):
    (name,format) = filename.split(".")
    if(format !="png"):
        print ("error: not a png")
        return 0

    basemode = Image.open(folder+filename)
    scale = basemode.size[0]
    if scale != basemode.size[1]:
        print("Error: none square image :")
    puissanceenieme = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == scale:
            puissanceenieme = 1
            break
    if (puissanceenieme == 0):
        print("square dimension must be 2^n+1")
        return 0

    datah = list(basemode.getdata())
    datah = [datah[k][0] for k in range(0, len(datah))]
    dirt = 200
    water = 50
    grass = 150
    dirtRmax = 130
    dirtRmin = 90
    dirtGmax = 70
    dirtGmin = 40
    grass_tmax = 175
    grass_tmin = 140
    ga = (grass_tmin - grass_tmax)/(grass-1-water)
    gb = ga * water + grass_tmax

    Ra = (dirtRmin - dirtRmax)/(dirt-1-grass)
    Ga = (dirtGmin - dirtGmax)/(dirt-1-grass)
    Rb = -Ra * grass + dirtRmax
    Gb = -Ga * grass + dirtGmax

    print("creation de la map texturé non mixé")
    imtext = [(0,0,0) for k in range(scale*scale)]
    for x in range(scale):
        for y in range(scale):
            if (datah[x+y*scale] < water):##water
                imtext[x + y * scale] = (0,int(125 *(0.5+datah[x+y*scale]/75*0.5)), int(255 *(0.5+datah[x+y*scale]/75*0.5)))
            elif (datah[x+y*scale] < grass): ## grass
                imtext[x + y * scale] = (45,int(ga*datah[x+y*scale]+gb),22)
            elif (datah[x+y*scale] < dirt): ## dirt
                imtext[x + y * scale] = (int(Ra*datah[x+y*scale]+Rb),int(Ga*datah[x+y*scale]+Gb),0)
            else:
                imtext[x + y * scale] = (255,255,255)
    imgOuttext = Image.new('RGB', (scale, scale))
    imgOuttext.putdata(imtext)
    imgOuttext.save(folder+"UV{}6.png".format(name))


UV("C:/Users/BEN/Pictures/ARDA_Project/","Heigthmap.png")