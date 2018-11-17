from PIL import Image
from io import StringIO

## De l'image au binaire

def ImageToBinary(image="lena.jpg"):
    # with open(image, "rb") as imageFile:
    #     f = imageFile.read()
    #     print("f: {0}".format(f))
    # b = f
    # donnees_image=[]
    # for i in range(len(b)):
    #     donnees_image.append(bin(b[i])[2:])
    # return (donnees_image)
    basemode = Image.open(image)
    data = list(basemode.getdata())
    print(data)
    datah = []
    for k in range (len(data)):
        datah += [data[k][0]]
        datah +=[data[k][1]]
        datah +=[data[k][2]]
    print(bytes(datah))
    b = bytes(datah)
    donnees_image=[]
    for i in range(len(b)):
        donnees_image.append(bin(b[i])[2:])
    return (donnees_image)
## Protocole

# Début de la transmission
begin=["1111111"]

# Fin de la transmission
end=["1110111"]
#Ces deux suite de bits définissent le début et la fin de la transmission par fibre optique

# Transmission

# transformer le 0 en un créneau de largeur 1 unités et 2 unités de chaque côté pour séparer du bit suivant (00100)
# transformer le 1 en deux créneaux successifs (01010)
# on a ainsi la meme largeur pour le 0 et le 1. Il faudrait des erreurs sur 3 bits pour qu'il y ai une erreur sur le symbole.

#dans le signal il y a des symboles qui sont des chaines de bits de longueur variable. On sépare chaque symbole par un séparateur ('111')

separateur="111"

def BinToStr(donnees_image, data=[]):
    bitsTransmission=[]
    bitsTransmission.append(begin)
    for i in donnees_image:
        chaineIntermédiaire=[]
        chaineIntermédiaire.append(separateur)
        for k in range(len(i)):
            if i[int(k)]=='0':
                chaineIntermédiaire.append('00100')
            else :
                chaineIntermédiaire.append('01010')
        chaineIntermédiaire.append(separateur)
        bitsTransmission.append(chaineIntermédiaire)
    bitsTransmission.append(end)    
    #print(bitsTransmission[:9])
    return(bitsTransmission)

#on a present les bits qui vont passer par la fibre optique on commence par supposer que le canal ne fait pas d'erreur

        
### Du flux binaire a l'image

#on receptionne le flux binaire à la sortie de la fibre optique.

def StrToBin(bitsTransmission):
    bitsReconstitues=[]
    for i in range(len(bitsTransmission)):
        if len(bitsTransmission[i])==1:
            if bitsTransmission=='1111111':
                print('Debut de la chaine')
            elif bitsTransmission=='1110111':
                print('Fin de la chaine')
        elif len(bitsTransmission[i])>1:
            nouveauSymbole=''
            for k in bitsTransmission[i]:
                if k=='00100':
                    nouveauSymbole+='0'
                elif k=='01010':
                    nouveauSymbole+='1'
            bitsReconstitues.append(nouveauSymbole)
    #print(bitsReconstitues[:3])
    return(bitsReconstitues)
       
       
# On a réussi à reconstituer les donnees binaires, on peut maintenant passer a la reconstitution de l'image de départ

def BinToImage(bitsReconstitues):
    donneesImageReconstitues=[]
    donnesEnBytes=b""
    im = Image.open("C:/Users/BEN/Pictures/ARDA_Project/boby2.png")
    width, height = im.size
    for i in range(len(bitsReconstitues)):
        donnesEnBytes+=int(bitsReconstitues[i],2).to_bytes(1, byteorder='big')
    print(donnesEnBytes)
    # imageReconstituee = Image.open(io.BytesIO(donnesEnBytes))
    # imageReconstituee.show()
    #dataBytesIO = io.BytesIO(donnesEnBytes)
    #PIL.Image.frombytes(mode, size, data, decoder_name='raw', *args)
    #imageReconstituee = Image.open(io.StringIO(donnesEnBytes))
    #Image.open(dataBytesIO)
    k = Image.frombytes('RGB', (width, height), donnesEnBytes, decoder_name='raw')
    k.save("C:/Users/BEN/Pictures/ARDA_Project/boby3.png")

def main():
    bob = BinToStr(ImageToBinary("C:/Users/BEN/Pictures/ARDA_Project/boby2.png"), data=[])
    code = StrToBin(bob)
    BinToImage(code)

main()
        
        


