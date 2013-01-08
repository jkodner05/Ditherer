from PIL import Image
from random import randint
import sys, getopt

def serpentine_fs(num_colors, scale, color, filename, outname):
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

def halftone(num_colors, scale, color, filename, outname):
    image = Image.open(filename)
    owidth, oheight = image.size
    image = image.resize((owidth/scale,oheight/scale))
    width, height = image.size
    pic = image.load()
    matrix = ((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
    matrix = ((12, 11, 10, 31, 30,  9,  8,  7),
              (13, 33, 32, 47, 46, 29, 28,  6),
              (14, 34, 48, 57, 56, 45, 27,  5),
              (35, 49, 58, 63, 62, 55, 44, 26),
              (36, 50, 59, 60, 61, 54, 43, 25),
              (15, 37, 51, 52, 53, 42, 24,  4),
              (16, 38, 39, 40, 41, 22, 23,  3),
              (17, 18, 19, 20, 21,  0,  1,  2))
    if not color:
        pic = greyscale(image)
    else:
        pic = image.load()
    for r in range(0,width):
        for c in range(0, height):
            pic[r,c] = tuple([(val+(63-matrix[r%8][c%8])*num_colors/64)*2/3 for val in pic[r,c]])
            pic[r,c] = palettize(pic[r, c], num_colors)
    image = image.resize((owidth,oheight))
    image.save(outname)

def stucki(num_colors, scale, color, filename, outname):
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
                pic[x,y+1] = tuple([int(pic[x,y+1][i] + (8.0/42)*error[i]) for i in range(0,3)])
                if x < width - 1:
                    pic[x+1,y+1] = tuple([int(pic[x+1,y+1][i] + (4.0/42)*error[i]) for i in range(0,3)]) 
                    if x < width - 2:
                        pic[x+2,y+1] = tuple([int(pic[x+2,y+1][i] + (2.0/42)*error[i]) for i in range(0,3)])
                if x > 0:
                    pic[x-1,y+1] = tuple([int(pic[x-1,y+1][i] + (4.0/42)*error[i]) for i in range(0,3)])
                    if x > 1:
                        pic[x-2,y+1] = tuple([int(pic[x-2,y+1][i] + (2.0/42)*error[i]) for i in range(0,3)])
                if y < height - 2:
                    pic[x,y+2] = tuple([int(pic[x,y+2][i] + (4.0/42)*error[i]) for i in range(0,3)])
                    if x < width - 1:
                        pic[x+1,y+2] = tuple([int(pic[x+1,y+2][i] + (2.0/42)*error[i]) for i in range(0,3)])
                        if x < width - 2:
                            pic[x+2,y+2] = tuple([int(pic[x+2,y+2][i] + (1.0/42)*error[i]) for i in range(0,3)])
                    if x > 0:
                        pic[x-1,y+2] = tuple([int(pic[x-1,y+2][i] + (2.0/42)*error[i]) for i in range(0,3)])
                        if x > 1:
                            pic[x-2,y+2] = tuple([int(pic[x-2,y+2][i] + (1.0/42)*error[i]) for i in range(0,3)])
            if x < width - 1:
                pic[x+1,y] = tuple([int(pic[x+1,y][i] + (8.0/42)*error[i]) for i in range(0,3)])
                if x < width - 2:
                    pic[x+2,y] = tuple([int(pic[x+2,y][i] + (4.0/42)*error[i]) for i in range(0,3)])

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

def demo(depth, scale, input):
    output_verbose(depth,scale,False,input,"demo_floyd-steinberg_mono.png", "floyd_steinberg")
    floyd_steinberg(depth,scale,False,input,"demo_floyd-steinberg_mono.png")
    output_verbose(depth,scale,True,input,"demo_floyd-steinberg_color.png", "floyd_steinberg")
    floyd_steinberg(depth,scale,True,input,"demo_floyd-steinberg_color.png")
    output_verbose(depth,scale,False,input,"demo_threshold_mono.png", "threshold")
    threshold(depth,scale,False,input,"demo_threshold_mono.png")
    output_verbose(depth,scale,True,input,"demo_threshold_color.png", "threshold")
    threshold(depth,scale,True,input,"demo_threshold_color.png")
    output_verbose(depth,scale,False,input,"demo_halftone_mono.png", "halftone")
    halftone(depth,scale,False,input,"demo_halftone_mono.png")
    output_verbose(depth,scale,True,input,"demo_halftone_color.png", "halftone")
    halftone(depth,scale,True,input,"demo_halftone_color.png")
    output_verbose(depth,scale,False,input,"demo_serpentine_mono.png", "serpentine_fs")
    serpentine_fs(depth,scale,False,input,"demo_serpentine_mono.png")
    output_verbose(depth,scale,True,input,"demo_serpentine_color.png", "serpentine_fs")
    serpentine_fs(depth,scale,True,input,"demo_serpentine_color.png")
    output_verbose(depth,scale,False,input,"demo_random_mono.png", "random")
    random(depth,scale,False,input,"demo_random_mono.png")
    output_verbose(depth,scale,True,input,"demo_random_color.png", "random")
    random(depth,scale,True,input,"demo_random_color.png")
    output_verbose(depth,scale,False,input,"demo_stucki_mono.png", "stucki")
    stucki(depth,scale,False,input,"demo_stucki_mono.png")
    output_verbose(depth,scale,True,input,"demo_stucki_color.png", "stucki")
    stucki(depth,scale,True,input,"demo_stucki_color.png")
    output_verbose(depth,scale,False,input,"demo_bayer2x2_mono.png", "bayer2x2")
    bayer2x2(depth,scale,False,input,"demo_bayer2x2_mono.png")
    output_verbose(depth,scale,True,input,"demo_bayer2x2_color.png", "bayer2x2")
    bayer2x2(depth,scale,True,input,"demo_bayer2x2_color.png")
    output_verbose(depth,scale,False,input,"demo_bayer4x4_mono.png", "bayer4x4")
    bayer4x4(depth,scale,False,input,"demo_bayer4x4_mono.png")
    output_verbose(depth,scale,True,input,"demo_bayer4x4_color.png", "bayer4x4")
    bayer4x4(depth,scale,True,input,"demo_bayer4x4_color.png")


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
    outpput = ""
    verbose = False
    run_demo = False
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
            run_demo = True
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
    if run_demo:
        demo(255/depth, scale, input)
        sys.exit()
    if type == "floyd-steinberg":
        floyd_steinberg(255/depth, scale, color, input, output)
    elif type == "threshold":
        threshold(255/depth, scale, color, input, output)
    elif type == "serpentine_fs":
        serpentine_fs(255/depth, scale, color, input, output)
    elif type == "random":
        random(255/depth, scale, color, input, output)
    elif type == "bayer2x2":
        bayer2x2(255/depth, scale, color, input, output)
    elif type == "bayer4x4":
        bayer4x4(255/depth, scale, color, input, output)
    elif type == "stucki":
        stucki(255/depth, scale, color, input, output)
    elif type == "halftone":
        halftone(255/depth, scale, color, input, output)
    else:
        print "Invalid method!"
        help()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
