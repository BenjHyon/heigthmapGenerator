from PIL import ImageFilter, Image
import matplotlib.pyplot as plt
import math

def main(filename):
    Img = Image.open(filename)
    size = Img.size[0]
    if size != Img.size[1]:
        print("Error : Image is not square !")
    OdP = 0
    for k in range(0, 500):
        if math.pow(2, k) + 1 == size:
            OdP = k
            break

    if (OdP == 0):
        print("Square dimension must be 2^n+1")
        return 0

    print("size : {} = 2^{} + 1".format(size,OdP))
    print("retrieving pixels ...")
    datah = list(Img.getdata())
    Img.close()

    print("analysing ...")
    rep = [0 for k in range(256)]
    for k in range(size*size):
        rep[datah[k][0]]+=1
    for k in range(256):
        rep[k] =rep[k]/(size*size)*100
    print("results:")
    plt.plot(rep)
    plt.show()

main("C:/Users/BEN/Pictures/ARDA_Project/blurred3.png")