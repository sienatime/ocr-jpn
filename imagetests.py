from PIL import Image
import code

def threshold_image(im):
    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(im.getpixel((j,i)))
        pixel_vals.append( l )

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    return im

def save_image(im, filename, filetype):
    im.save(filename, filetype)

def resize_and_crop_image(im):
    size = 128, 128
    #if we don't resize the image, it's like, a lot of pixels to deal with...
    im.thumbnail(size)

    out = im.point(lambda i: i * 2)

    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(out.getpixel((j,i)))
        pixel_vals.append( l )

    #umm okay yeah so if the ENTIRE ROW is white, we need that info

    nonwhiterows = []

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                nonwhiterows.append((j,i))
                out.putpixel( (j,i), (0) )
            else:
                out.putpixel( (j,i), (255) )

    #so now that I have a list of nonwhite rows, I need to find the extreme x AND y values. so I probably need a list of coordinates anyway. and then i can compare the coordinates to each other. so i should probably have a list of tuples or something.

    upper = nonwhiterows[0][1]
    lower = nonwhiterows[-1][1]

    min_x = im_x
    max_x = 0

    for x, y in nonwhiterows:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

    box = (min_x, upper, max_x+1, lower+1)

    region = out.crop(box)

    return region

def compare_to_template(im, template):
    im = im.resize(template.size)
    im_x, im_y = im.size
    tmp_x, tmp_y = template.size

    #now analyze how similar these two images are

    #so probably like, return a difference for each pixel and then do some math and shit. the point() function takes another function as a param and runs that function on each of the pixels. i guess i could compare something completely similar and something completely dissimilar to get my threshold...


    im_pixel_vals = []
    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range(im_x):
            l.append(im.getpixel((j,i)))
        im_pixel_vals.append( l )

    tmp_pixel_vals = []

    for i in range(tmp_y):
        l = []
        for j in range(tmp_x):
            l.append(template.getpixel((j,i)))
        tmp_pixel_vals.append(l)

    differences = []

    for i in range(len(im_pixel_vals)):
        for j in range(len(im_pixel_vals[i])):
            differences.append( abs(im_pixel_vals[i][j] - tmp_pixel_vals[i][j]) )

    for i in range(len(differences)):
        if differences[i] == 255:
            differences[i] = 1

    total = sum(differences)

    # code.interact(local=locals())

    return total

def convert_to_percentage(l):
    return [ item/255.0 * 100 for item in l ]

def main():
    im = Image.open("o.bmp").convert("L")
    new_image = resize_and_crop_image(im)
    # new_image.show()

    template = Image.open("printot.bmp").convert("L")
    mincho = Image.open("minchoa.bmp").convert("L")

    print compare_to_template(new_image, template)

if __name__ == "__main__":
    main()