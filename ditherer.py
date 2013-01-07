from PIL import Image
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
    r = int(pixel[0]+pixel[0]*.5) / nc * nc
    g = int(pixel[1]+pixel[1]*.5) / nc * nc
    b = int(pixel[2]+pixel[2]*.5) / nc * nc
    return (r,g,b)

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
        opts, args = getopt.getopt(argv, "i:o:r:d:m:hcv",["input=", "output=", "resolution=","depth=","method=","help","color","verbose"])
    except getopt.GetoptError:
        print "invalid args"
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-r", "--resolution"):
            scale = arg
        elif opt in ("-t", "--depth"):
            depth = arg
        elif opt in ("-m", "--method"):
            type = arg
        elif opt in ("-c", "--color"):
            color = True
        elif opt in ("-v", "--verbose"):
            verbose = True
    if verbose:
        output_verbose(depth, scale, color, input, output, type)
    if type == "floyd-steinberg":
        floyd_steinberg(255/depth, scale, color, input, output)
    elif type == "threshold":
        threshold(255/depth, scale, color, input, output)
    elif type == "boustrophedonic":
        print type
        boustrophedonic(255/depth, scale, color, input, output)

if __name__ == "__main__":
    main(sys.argv[1:])
