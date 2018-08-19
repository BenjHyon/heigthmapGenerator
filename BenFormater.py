from PIL import Image
import math

def Formater(folder,filename):
    (name,format) = filename.split(".")
    if(format != "png"):
        print ("erreur: png attendu")
        return 0

    basemode = Image.open(folder+filename)
    scale = basemode.size[0]
    if scale != basemode.size[1]:
        print("Erreur ! l'image fourni n'est pas carré :")
    #check les dimensions:
    puissanceenieme = 0
    OdP = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == scale:
            puissanceenieme = 1
            OdP = k
            break
    if (puissanceenieme == 0):
        print("les dimensions du carrée ne sont pas bonnes, veuillez selectionner une autre ebauche")
        return 0

    datah = list(basemode.getdata())
    datah = [datah[k][0] for k in range(0, len(datah))]
    bytefile = open(folder+"/map{}.ben".format(name),'wb')
    hearder = [1,2,3]
    bytefile.write(bytes(hearder))
    bytefile.write(bytes([OdP]))
    bytefile.write(bytes(datah))
    bytefile.close()

Formater("C:/Users/BEN/Pictures/ARDA_Project/","hm2.png")