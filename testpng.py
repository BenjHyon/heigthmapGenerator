import png
#f = open('E:/ramp.png', 'wb')      # binary mode is important
#w = png.Writer(255, 1, greyscale=True)
#w.write(f, [range(256)])
#f.close()

p = [[255,0,0,0,255,0,0,0,255],
     [128,0,0, 0,128,0, 0,0,128]]
f = open('E:/snatch2.png', 'wb')
w = png.Writer(3, 2)
w.write(f, p) ; f.close()