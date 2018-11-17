from PIL import Image, ImageFilter

#set all pixel with color different from black or whit to grey

def main(filename):
    ## ouverture et verification

    basemode = Image.open(filename)
    datah = list(basemode.getdata())
    for i in range(len(datah)):
        if datah[i] != (255,255,255) and datah[i] != (0,0,0):
            datah[i] = (125,125,125)
    imgGreyed = Image.new('RGB', (2049, 2049))
    imgGreyed.putdata(datah)
    imgGreyed.save("C:/Users/BEN/Pictures/ARDA_Project/hm1.png")




main("C:/Users/BEN/Pictures/ARDA_Project/noirBlanc.png")