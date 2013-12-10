  # -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from sys import argv
from islands import find_islands
import psycopg2
from os import listdir
from time import clock
import split_images

AVG_BIG_TEMPLATE_HEIGHT = 80
THRESHOLD_OFFSET = 20
verbose = True
LAST_TIME = None
TOTAL_TIME = []
ISLAND_MODE = True
mode = None

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

if len(argv) == 3:
    script, img, mode = argv

def open_threshold_save(im_name, save_name):
    im = Image.open(im_name).convert("L")
    new_image = threshold_image(im)
    save_image(new_image, save_name, "BMP")
    new_image.show()

def save_image(im, filename, filetype):
    im.save(filename, filetype)

def sample_corners(im):
    global THRESHOLD_OFFSET
    #take a 9x9 sample of the corners. with any luck, these will be mostly representative of the background color.
    pixel_data = list(im.getdata())
    im_avg = sum(pixel_data)/len(pixel_data) - THRESHOLD_OFFSET
    im_x, im_y = im.size
    crop_size = 3

    corner1 = im.crop( (0, 0, crop_size, crop_size) )
    corner2 = im.crop( (im_x - crop_size, 0, im_x, crop_size) )
    corner3 = im.crop( (0, im_y - crop_size, crop_size, im_y) )
    corner4 = im.crop( (im_x - crop_size, im_y - crop_size, im_x, im_y) )

    corner_data = list(corner1.getdata()) + list(corner2.getdata()) + list(corner3.getdata()) + list(corner4.getdata())

    corner_avg = sum(corner_data)/len(corner_data) - THRESHOLD_OFFSET

    #if the average value of the corners is less than the average value of the image, it means the whole image is light so perhaps we should invert.
    if corner_avg < im_avg:
        return True
    else:
        return False

def resize_image(im, avg):
    im_x, im_y = im.size
    global AVG_BIG_TEMPLATE_HEIGHT
    global AVG_SMALL_TEMPLATE_HEIGHT

    big_ratio = float(AVG_BIG_TEMPLATE_HEIGHT)/im_y

    if big_ratio > 1:
        out = im.resize((int(im_x*big_ratio), int(im_y*big_ratio)), Image.ANTIALIAS)
    else:
        size = AVG_BIG_TEMPLATE_HEIGHT, AVG_BIG_TEMPLATE_HEIGHT
        im.thumbnail(size, Image.ANTIALIAS)
        out = im

    return out

def threshold_image(im, avg):
    im_x, im_y = im.size
    black_pixels = []

    # threshold the image
    for i in range(im_y):
        for j in range(im_x):
            # if the pixel value is LOWER than the average, turn to black
            if im.getpixel((j,i)) < avg:
                black_pixels.append((j,i))
                im.putpixel( (j,i), (0) )
            # otherwise turn it white
            else:
                im.putpixel( (j,i), (255) )

    # blackpixels -- min? 
    return im, black_pixels

def crop_image(im, black_pixels):
    im_x, im_y = im.size
    # the values of black_pixels are tuples like (x, y) and have all the coordinates that are black in them.
    if len(black_pixels) > 0:
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
    else:
        return im

def process_image(im):
    pixel_data = list(im.getdata())
    global THRESHOLD_OFFSET

    #find the average value of the image (sum of all values/number of pixels) and subtract 20, for anti-aliasing. anything below this number becomes black (0), and anything above becomes white (255).
    avg = sum(pixel_data)/len(pixel_data) - THRESHOLD_OFFSET
    out = resize_image(im, avg)
    thrs, black_pixels = threshold_image(out, avg)

    return crop_image(thrs, black_pixels)

def compare_to_template(im, template):
    #I've been finding it better to resize the template to the image at hand, rather than the other way around, although at this point the image at hand should already be pretty close in size to most of the templates.

    template = template.resize(im.size)

    im_x, im_y = im.size
    tmp_x, tmp_y = template.size

    im_pixel_vals = list(im.getdata())

    tmp_pixel_vals = list(template.getdata())

    #xor the values of both images. the pixels that are different will give us a "score" as to how different the images are. lower scores mean more similarity.
    differences = [ int(abs((tmp_pixel_vals[i] - im_pixel_vals[i]))/255) for i in range(len(im_pixel_vals)) ]

    total = sum(differences)/float(len(im_pixel_vals))

    return total

def run_thru_templates_local(path, im):
    templates = listdir(path)
    scores = []

    for filename in templates:
        try:
            template = Image.open(path+filename).convert("L")
            if "mincho" in path:
                font = "mincho"
            elif "gothic" in path:
                font = "gothic"
            scores.append( (filename, compare_to_template(im, template), font) )
        except(IOError):
            print "couldn't open file:", filename
        
    return scores

def run_thru_templates_db(im, island_range, white_lower, im_white):
    char_type = 'kanji'

    if mode:
        if mode == "smkanji":
            char_type = "kanji"
        elif mode == "kanji" or mode == "hiragana" or mode =="katakana":
            char_type = mode

    if verbose:
        print "test image islands", im_white
    # im.show()

    if char_type != 'kanji':
        # if it's the kana, just search through those by themselves, it's fast enough. umm should i return both fonts for the kana? not sure.
        cur.execute("SELECT code, img_path from characters where char_type = %s and img_size = %s;", (char_type, 'big'))
    else:
        global ISLAND_MODE
        if ISLAND_MODE:
            if island_range == 0:
                #experimenting with just using the gothic font. actually mincho doesn't have the small whites column so... yeah...........
                if verbose:
                    print "white islands", im_white
                cur.execute("SELECT code, img_path from characters where font = 'gothic' and char_type = %s and img_size = 'big' and sm_whites = %s;", (char_type, im_white))
            else:
                if verbose:
                    print "searching white islands", white_lower, im_white+island_range, char_type
                cur.execute("SELECT code, img_path from characters where font = 'gothic' and char_type = %s and img_size = 'big' and (sm_whites = %s or sm_whites = %s);", (char_type, white_lower, im_white+island_range))

        else:
            cur.execute("SELECT code, img_path from characters where img_size = 'big' and font = 'gothic' and sm_whites is not null;", (char_type))
    
    matches = cur.fetchall()

    if not matches:
        raise LookupError("Didn't select any rows from the database.")

    if verbose:
        print "selected %d rows" % len(matches)

    scores = []
    for row in matches:
        code, img_path = row
        template = Image.open(img_path).convert("L")
        the_score = compare_to_template(im, template)
        scores.append( (code, the_score) )

    return scores

def run_thru_kana(im):
    cur.execute("SELECT code, img_path, font from characters where font = 'gothic' and (char_type = 'hiragana' or char_type = 'katakana');")
    matches = cur.fetchall()

    scores = []
    for row in matches:
        code, img_path, font = row
        template = Image.open(img_path).convert("L")
        the_score = compare_to_template(im, template)
        scores.append( (code, the_score, font) )

    return scores

def search_similar_chars(im, candidates):
    #candidates is a list of scores, which are a tuple like (code, score)
    print candidates

    if not candidates:
        return []

    highest = candidates[0][0]

    already_searched = {}

    for score_tup in candidates:
        already_searched[score_tup[0]] = 1

    print "Similarity seed:", unichr(highest)

    cur.execute("SELECT similar_code, similar_code_path from similarities where code = %s;", (highest,))

    matches = cur.fetchall()
    
    if matches:
        sim_scores = []
        for row in matches:
            sim_code, sim_img_path = row
            if not already_searched.get(sim_code, None):
                template = Image.open(sim_img_path).convert("L")
                the_score = compare_to_template(im, template)
                sim_scores.append( (sim_code, the_score) )

        sorted_sim_scores = sorted(sim_scores, key=lambda score: score[1]) 

        all_scores = candidates + sorted_sim_scores
        all_scores = sorted(all_scores, key=lambda score: score[1])

        return [ unichr(all_scores[i][0]) for i in range(3)]
    else:
        return [ unichr(candidates[i][0]) for i in range(3)]

def search_local(input_imgs, paths):
    for image in input_imgs:
        black, white = find_islands(image)
        scores = []
        for path in paths:
            scores = scores + run_thru_templates_local(path, image)
        sorted_scores = sorted(scores, key=lambda score: score[1]) 
        print_time()
        print"***********WINNER***********", unichr(int(sorted_scores[0][0].split(".")[0])), sorted_scores[0][1], sorted_scores[0][2]

def search_db(input_imgs):
    print_time()

    valid_white_vals = set([25,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0])

    return_vals = []
    for image in input_imgs:
        #image.show()
        im_black, im_white = find_islands(image)

        kana_scores = run_thru_kana(image)
        sorted_kana_scores = sorted(kana_scores, key=lambda score: score[1]) 

        high_kana_score = sorted_kana_scores[0][1]
        print "highest kana score", unichr(sorted_kana_scores[0][0]), high_kana_score

        adjust_these = []

        if high_kana_score < 0.3:
            print "kana score was good enough", high_kana_score
            adjust_these += sorted_kana_scores[:3]

        final_score = 1
        island_range = 0
        white_upper = im_white

        while white_upper not in valid_white_vals:
            #pick another one
            print "not a valid number of white islands"
            white_upper -= 1

        sorted_scores = []

        while final_score > 0.3:
            print "searching..."
            white_lower = im_white-island_range
            while white_lower not in valid_white_vals:
                #pick another one
                print "not a valid number of white islands"
                white_lower -= 1
            if white_lower <= 1:
                print "GIVING UP"
                break

            scores = []
            scores = scores + run_thru_templates_db(image, island_range, white_lower, white_upper)

            sorted_scores = sorted(scores, key=lambda score: score[1]) 
            island_range += 1
            final_score = sorted_scores[0][1]

            if not ISLAND_MODE:
                break
    
        adjust_these += sorted_scores[:3]

        adjusted_candidates = search_similar_chars(image, sorted(adjust_these, key=lambda score: score[1]))
        return_vals.append(adjusted_candidates)

        print_time()

    print_total_time()

    for row in return_vals:
        if row:
            print row[0], row[1], row[2]

    return return_vals

def print_time():
    global LAST_TIME
    global TOTAL_TIME
    this_time = clock()
    if LAST_TIME:
        elapsed = this_time - LAST_TIME
        LAST_TIME = this_time
        print "Time elapsed", elapsed
        TOTAL_TIME.append(elapsed)
        return
    else:
        LAST_TIME = this_time
        print "Starting the clock", LAST_TIME

def print_total_time():
    global TOTAL_TIME
    print "\nTotal time:", sum(TOTAL_TIME)

def ocr_image(inp):
    im = inp.convert("L")
    im_x, im_y = im.size

    if sample_corners(im):
        print "inverting image"
        im = ImageChops.invert(im)

    # experimenting with adding some extra buffer but it doesn't actually seem to make a consistent difference in accuracy.
    # im = ImageOps.expand(im, border=1, fill=255)

    new_image = process_image(im)

    new_image_x, new_image_y = new_image.size

    input_imgs = [new_image]

    if new_image_x / 1.5 > new_image_y:
        input_imgs = []
        input_imgs = split_images.split_images(new_image, "wide")
    elif new_image_y / 1.5 > new_image_x:
        input_imgs = []
        input_imgs = split_images.split_images(new_image, "tall")

    for i in reversed(range(len(input_imgs))):
        split_x, split_y = input_imgs[i].size

        if im_x/split_x > 2 or im_y/split_y > 2:
            print "deleted small image!"
            del input_imgs[i]

    return search_db(input_imgs)

def main():
    #from argv use img. L is black and white mode.
    print_time()
    im = Image.open(img)

    if mode == "hiragana":
        paths = ["../templates/hiragana/gothic/", "../templates/hiragana/mincho/"]
    elif mode == "katakana":
        paths = ["../templates/katakana/gothic/", "../templates/katakana/mincho/"]
    elif mode == "kanji":
        # paths = [ "../templates/kanji/mincho/", "../templates/kanji/mincho extra/", "../templates/kanji/gothic/", "../templates/kanji/gothic extra/"]
        paths = [ "../templates/kanji/mincho/", "../templates/kanji/gothic/"]
    elif mode =="smkanji":
        paths = [ "../templates/kanji/small mincho/", "../templates/kanji/small gothic/"]
    else:
        print "Please specify hiragana, katakana, kanji, or smkanji."

    # search_local(input_imgs, paths)

    results = ocr_image(im)

    print "**********"
    for result in results:
        print result[0][0], # this is the top score
    
    print_total_time()

if __name__ == "__main__":
    main()