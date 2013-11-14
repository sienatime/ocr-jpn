  # -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageChops
from sys import argv
from islands import find_islands
import psycopg2
# import code

AVG_TEMPLATE_HEIGHT = 80
THRESHOLD_OFFSET = 20

if len(argv) == 2:
    script, img = argv

def open_threshold_save(im_name, save_name):
    im = Image.open(im_name).convert("L")
    new_image = threshold_image(im)
    save_image(new_image, save_name, "BMP")
    new_image.show()

def save_image(im, filename, filetype):
    im.save(filename, filetype)

def sample_corners(im, im_avg):
    #take a 9x9 sample of the corners. with any luck, these will be mostly representative of the background color.
    im_x, im_y = im.size
    crop_size = 3

    corner1 = im.crop( (0, 0, crop_size, crop_size) )
    corner2 = im.crop( (im_x - crop_size, 0, im_x, crop_size) )
    corner3 = im.crop( (0, im_y - crop_size, crop_size, im_y) )
    corner4 = im.crop( (im_x - crop_size, im_y - crop_size, im_x, im_y) )

    corner_data = list(corner1.getdata()) + list(corner2.getdata()) + list(corner3.getdata()) + list(corner4.getdata())

    global THRESHOLD_OFFSET
    corner_avg = sum(corner_data)/len(corner_data) - THRESHOLD_OFFSET

    #if the average value of the corners is less than the average value of the image, it means the whole image is light so perhaps we should invert.
    if corner_avg < im_avg:
        return True
    else:
        return False

def resize_image(im, avg):
    if sample_corners(im, avg):
        print "inverting image"
        im = ImageChops.invert(im)

    im_x, im_y = im.size
    global AVG_TEMPLATE_HEIGHT
    ratio = float(AVG_TEMPLATE_HEIGHT)/im_y

    if ratio > 1:
        out = im.resize((int(im_x*ratio), int(im_y*ratio)), Image.ANTIALIAS)
    else:
        size = AVG_TEMPLATE_HEIGHT, AVG_TEMPLATE_HEIGHT
        im.thumbnail(size, Image.ANTIALIAS)
        out = im

    return out

def threshold_image(im, avg):
    im_x, im_y = im.size

    black_pixels = []

    # threshold the image
    for i in range(im_y):
        for j in range(im_x):
            if im.getpixel((j,i)) < avg:
                black_pixels.append((j,i))
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    # blackpixels -- min? 
    return im, black_pixels

def crop_image(im, black_pixels):
    im_x, im_y = im.size
    # the values of black_pixels are tuples like (x, y) and have all the coordinates that are black in them.
    upper = black_pixels[0][1] #this is the y value of the first black pixel
    lower = black_pixels[-1][1] #this is the y value of the last black pixel

    #this is just initializing these variables. min_x MUST be smaller than the width of the image, and max_x MUST be bigger than 0.
    min_x = im_x
    max_x = 0

    #find the lowest and highest x value of black pixels
    #could also probably sort this on the x values like I did in the scoring function, e.g. sort_by_x = sorted(black_pixels, key=lambda x: score[0]) 
    for x, y in black_pixels:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

    # the crop is exclusive so that is why we +1 to the 2nd set of coordinates. should probably watch im for index im-of-bounds here...
    box = (min_x, upper, max_x+1, lower+1)

    region = im.crop(box)

    return region

def process_image(im):
    pixel_data = list(im.getdata())
    global THRESHOLD_OFFSET

    #find the average value of the image (sum of all values/number of pixels) and subtract 20, for anti-aliasing. anything below this number becomes black (0), and anything above becomes white (255).
    avg = sum(pixel_data)/len(pixel_data) - THRESHOLD_OFFSET

    out = resize_image(im, avg)
    out, black_pixels = threshold_image(out, avg)

    return crop_image(out, black_pixels)

def compare_to_template(im, template):
    #I've been finding it better to resize the template to the image at hand, rather than the other way around, although at this point the image at hand should already be pretty close in size to most of the templates.

    template = template.resize(im.size)

    im_x, im_y = im.size
    tmp_x, tmp_y = template.size

    im_pixel_vals = list(im.getdata())

    tmp_pixel_vals = list(template.getdata())

    #xor the values of both images. the pixels that are different will give us a "score" as to how different the images are. lower scores mean more similarity.
    differences = [ int(abs((tmp_pixel_vals[i] - im_pixel_vals[i]))/255) for i in range(len(im_pixel_vals)) ]

    total = sum(differences)

    return total

def find_split_ranges(l):
    split_ranges = []
    slice_start = 0

    length = len(l)

    for i in range(length):
        # if i == 11:
        #     code.interact(local=locals())
        if i == length-1 or l[i] + 1 != l[i+1]:
            split_ranges.append( l[slice_start:i+1] )
            slice_start = i+1

    return split_ranges

def find_white_cols(im):
    x, y = im.size
    white_cols = []
    for i in range(x):
        if im.getpixel((i, 0)) == 255:
            for j in range(1, y):
                if im.getpixel(( i, j )) == 0:
                    break
            if j == y - 1:
                white_cols.append(i)
    return white_cols

def find_white_rows(im):
    x, y = im.size
    white_rows = []
    for i in range(y):
        if im.getpixel((0, i)) == 255:
            for j in range(1, x):
                if im.getpixel(( j, i )) == 0:
                    break
            if j == x - 1:
                white_rows.append(i)
    return white_rows

def split_images(im, direction):
    im_x, im_y = im.size
    
    final_images = []
    boxes = []
    start_x = 0
    start_y = 0
    
    if direction == "wide":
        white_cols = find_white_cols(im)
        split_ranges = find_split_ranges(white_cols)
        end = im_y

        for rng in split_ranges:
            boxes.append( (start_x, start_y, rng[0], end) )
            start_x = rng[-1] + 1

        boxes.append( (split_ranges[-1][-1], start_y, im_x, end) )

    elif direction == "tall":
        white_rows = find_white_rows(im)
        split_ranges = find_split_ranges(white_rows)
        end = im_x

        for rng in split_ranges:
            boxes.append( (start_x, start_y, end, rng[0]) )
            start_y = rng[-1] + 1

        boxes.append( ( start_x, split_ranges[-1][-1], end, im_y) )

    for box in boxes:
            cropped = im.crop(box)
            new_im = process_image(cropped)
            final_images.append(new_im)

    return final_images

def run_thru_templates(im):
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    im_black, im_white = find_islands(im)
    print "test image islands", im_black, im_white
    # im.show()
    # cur.execute("SELECT code, img_path from characters where blacks = %s and whites = %s;", (im_black, im_white))
    cur.execute("SELECT code, img_path from characters;")
    matches = cur.fetchall()
    print "selected %d rows" % len(matches)

    scores = []
    for row in matches:
        code, img_path = row
        template = Image.open(img_path).convert("L")
        scores.append( (code, compare_to_template(im, template)) )

    return scores

def parse_score(score):
    # score is a tuple constructed like (filename.bmp, score)
    # i would really like to wrap this in a try/catch in case unichr() freaks out
    return unichr(score[0])

def main():
    #from argv use img. L is black and white mode.
    im = Image.open(img).convert("L")
    new_image = process_image(im)

    new_image_x, new_image_y = new_image.size

    input_imgs = [new_image]

    if new_image_x / 1.5 > new_image_y:
        input_imgs = []
        input_imgs = split_images(new_image, "wide")
    elif new_image_y / 1.5 > new_image_x:
        input_imgs = []
        input_imgs = split_images(new_image, "tall")

    for image in input_imgs:
        # image.show()
        scores = []
        scores = scores + run_thru_templates(image)
        sorted_scores = sorted(scores, key=lambda score: score[1]) 
        print parse_score(sorted_scores[0]), sorted_scores[0][1]
        print parse_score(sorted_scores[1]), sorted_scores[1][1]
        print parse_score(sorted_scores[2]), sorted_scores[2][1]

if __name__ == "__main__":
    main()