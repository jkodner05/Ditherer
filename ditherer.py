from PIL import Image
from random import randint
import sys, getopt

def boustrophedonic(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
                
    for y in range(0, height):
        for x in range(0,width):
            if y % 2:
                x = width - x - 1
            old = pic[x,y]
            new = palettize(pic[x,y], num_colors)
            pic[x,y] = new
            error = [old[i] - n for i, n in enumerate(new)]
            if y % 2:
                if y < height - 1:
                    if x < width - 1:
                        pic[x+1,y+1] = tuple([int(pic[x+1,y+1][i] + (3.0/16)*error[i]) for i in range(0,3)])
                    if x > 0:
                        pic[x-1,y+1] = tuple([int(pic[x-1,y+1][i] + (1.0/16)*error[i]) for i in range(0,3)])
                    pic[x,y+1] = tuple([int(pic[x,y+1][i] + (5.0/16)*error[i]) for i in range(0,3)])
                if x > 0:
                    pic[x-1,y] = tuple([int(pic[x-1,y][i] + (7.0/16)*error[i]) for i in range(0,3)])
            else:
                if y < height - 1:
                    if x > 0:
                        pic[x-1,y+1] = tuple([int(pic[x-1,y+1][i] + (3.0/16)*error[i]) for i in range(0,3)])
                    if x < width - 1:
                        pic[x+1,y+1] = tuple([int(pic[x+1,y+1][i] + (1.0/16)*error[i]) for i in range(0,3)])
                    pic[x,y+1] = tuple([int(pic[x,y+1][i] + (5.0/16)*error[i]) for i in range(0,3)])
                if x < width - 1:
                    pic[x+1,y] = tuple([int(pic[x+1,y][i] + (7.0/16)*error[i]) for i in range(0,3)])
    image = image.resize((owidth,oheight))
    image.save(outname)

def bayer2x2(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    pic = image.load()
    matrix = ((1,3),(4,2))
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = tuple([(val+matrix[r%2][c%2]*num_colors/5)*2/3 for val in pic[r,c]])
            pic[r,c] = palettize(pic[r, c], num_colors)
    image = image.resize((owidth,oheight))
    image.save(outname)

def bayer4x4(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    pic = image.load()
    matrix = ((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = tuple([(val+matrix[r%4][c%4]*num_colors/16)*2/3 for val in pic[r,c]])
            pic[r,c] = palettize(pic[r, c], num_colors)
    image = image.resize((owidth,oheight))
    image.save(outname)


def floyd_steinberg(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
                
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
    image = image.resize((owidth,oheight))
    image.save(outname)

def threshold(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    pic = image.load()
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = palettize(pic[r, c], num_colors)
    image = image.resize((owidth,oheight))
    image.save(outname)

def random(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = tuple([val+randint(-160,159) for val in pic[r,c]])
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = palettize(pic[r, c], num_colors)
    image = image.resize((owidth,oheight))
    image.save(outname)


def greyscale(image):
    width, height = image.size
    pic = image.load()
    for x in range(0,width):
        for y in range(0, height):
            color = (pic[x,y][0]+pic[x,y][1]+pic[x,y][2])/3
            pic[x,y] = (color,color,color)
    return pic

def palettize(pixel, nc):
    """truncate pixel to nearest palette color"""
    r = int(pixel[0]*3/2) / nc * nc
    g = int(pixel[1]*3/2) / nc * nc
    b = int(pixel[2]*3/2) / nc * nc
    return (r,g,b)

def demo(input):
    floyd_steinberg(255,1,False,input,"demo_floyd-steinberg_mono.png")
    floyd_steinberg(255,1,True,input,"demo_floyd-steinberg_color.png")
    threshold(255,1,False,input,"demo_threshold_mono.png")
    threshold(255,1,True,input,"demo_threshold_color.png")
    boustrophedonic(255,1,False,input,"demo_serpentine_mono.png")
    boustrophedonic(255,1,True,input,"demo_serpentine_color.png")
    random(255,1,False,input,"demo_random_mono.png")
    random(255,1,True,input,"demo_random_color.png")
    bayer2x2(255,1,False,input,"demo_bayer2x2_mono.png")
    bayer2x2(255,1,True,input,"demo_bayer2x2_color.png")
    bayer4x4(255,1,False,input,"demo_bayer4x4_mono.png")
    bayer4x4(255,1,True,input,"demo_bayer4x4_color.png")


def help():
    print "valid processing methods:"
    print "\tboustrophedonic\n\tfloyd-steinberg\n\tthreshold"

def output_verbose(depth, scale, color, input, output, type):
    print "processing image:\t", input, "to", output
    print "processing method:\t", type
    print "color:\t\t\t", str(color)
    print "color depth:\t\t", depth
    print "resolution:\t\t", "1 /", scale
    return

def main(argv):
    type = "floyd-steinberg"
    scale = 1
    depth = 1
    color = False
    input = ""
    output = ""
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "i:o:r:d:m:hcvt",["input=", "output=", "resolution=","depth=","method=","help","color","verbose", "demo"])
    except getopt.GetoptError:
        print "invalid args"
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        if opt in ("-t", "--demo"):
            demo(input)
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-r", "--resolution"):
            scale = arg
        elif opt in ("-d", "--depth"):
            depth = arg
        elif opt in ("-m", "--method"):
            type = arg
        elif opt in ("-c", "--color"):
            color = True
        elif opt in ("-v", "--verbose"):
            verbose = True
    depth = int(depth)
    scale = int(scale)
    if verbose:
        output_verbose(depth, scale, color, input, output, type)
    if type == "floyd-steinberg":
        floyd_steinberg(255/depth, scale, color, input, output)
    elif type == "threshold":
        threshold(255/depth, scale, color, input, output)
    elif type == "boustrophedonic":
        boustrophedonic(255/depth, scale, color, input, output)
    elif type == "boustrophedonic":
        boustrophedonic(255/depth, scale, color, input, output)
    elif type == "random":
        random(255/depth, scale, color, input, output)
    elif type == "bayer2x2":
        bayer2x2(255/depth, scale, color, input, output)
    elif type == "bayer4x4":
        bayer4x4(255/depth, scale, color, input, output)
    else:
        print "Invalid method!"
        help()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
