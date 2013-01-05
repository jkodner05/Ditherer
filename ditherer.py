from PIL import Image

def floyd_steinberg(num_colors, filename, outname):
    image = Image.open(filename)
    width, height = image.size
    pic = image.load()
    for x in range(0,width):
        for y in range(0, height):
            color = (pic[x,y][0]+pic[x,y][1]+pic[x,y][2])/3
            pic[x,y] = (color,color,color)
    for y in range(0, height):
        for x in range(0,width):
            old = pic[x,y]
            new = palettize(pic[x,y], num_colors)
            pic[x,y] = new
            error = [old[i] - n for i, n in enumerate(new)]
            if y < height - 1:
                if x > 0:
                   pic[x-1,y+1] = tuple([int(pic[x-1,y+1][i] + (3.0/16)*error[i]) for i in range(0,3)])
                if x < width - 1:
                    pic[x+1,y+1] = tuple([int(pic[x+1,y+1][i] + (1.0/16)*error[i]) for i in range(0,3)])
                pic[x,y+1] = tuple([int(pic[x,y+1][i] + (5.0/16)*error[i]) for i in range(0,3)])
            if x < width - 1:
                pic[x+1,y] = tuple([int(pic[x+1,y][i] + (7.0/16)*error[i]) for i in range(0,3)])
                
    image.save(outname)

def threshold(num_colors, filename):
    image = Image.open(filename)
    width, height = image.size
    pic = image.load()
    for x in range(0,width):
        for y in range(0, height):
            color = (pic[x,y][0]+pic[x,y][1]+pic[x,y][2])/3
#            pic[x,y] = (color,color,color)
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = palettize(pic[r, c], num_colors)
    image.save("dith1.png")



def add_rgb(first, second):
    return tuple([second[i]+elem for i, elem in enumerate(first)])

def scale_rgb(factor, pixel):
    return tuple([int(factor*float(color)) for color in pixel])

def palettize(pixel, nc):
    """truncate pixel to nearest palette color"""
    r = int(pixel[0]+pixel[0]*.5) / nc * nc
    g = int(pixel[1]+pixel[1]*.5) / nc * nc
    b = int(pixel[2]+pixel[2]*.5) / nc * nc
    return (r,g,b)

floyd_steinberg(255,"kamille.png", "0.png")
floyd_steinberg(128,"kamille.png", "1.png")
floyd_steinberg(64,"kamille.png", "2.png")
floyd_steinberg(32,"kamille.png", "3.png")
floyd_steinberg(16,"kamille.png", "4.png")
floyd_steinberg(8,"kamille.png", "5.png")
floyd_steinberg(4,"kamille.png", "6.png")
floyd_steinberg(2,"kamille.png", "7.png")
floyd_steinberg(1,"kamille.png", "8.png")

#threshold(255,"Sphinx.png")
        
    
