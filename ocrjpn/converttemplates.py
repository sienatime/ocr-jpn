  # -*- coding: utf-8 -*-
from PIL import Image
import os
from recognize import save_image, crop_image

def threshold_image(im):
    im_x, im_y = im.size

    black_pixels = []

    # threshold the image
    for i in range(im_y):
        for j in range (im_x):
            #this is not the exact same function as in imagetests since we don't need to bother getting the average of the image since we already know what it is.
            if im.getpixel((j,i)) < 172:
                black_pixels.append((j,i))
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    return im, black_pixels

def make_templates(im, kanji):
    # you are going to want to change the WIDTH and HEIGHT of each character. use the grid in photoshop to help you.
    # you are also going to want to change the number of kanji per row (you mod by it around line 41)
    width = 150 #125 for mincho kanji, 150 for gothic, 200 for kana, 39 for small kanji
    height = 150 #145 for kanji, 150 for gothic, 150 for kana, 34 for small kanji
    origin = 0
    box = (0, 0, width, height)
    row = 1

    for i in range(1, len(kanji)+1):
        print i
        print box
        work = im.crop(box)

        new_image, black_pixels = threshold_image(work)
        new_work = crop_image(new_image, black_pixels)
        save_image(new_work, str(ord(kanji[i-1]))+".bmp", "BMP")

        if i % 6 == 0 and i != 0: #8 for mincho kanji, 6 for gothic, 5 for kana, 25 for small kanji
            #go to the next line
            box = (origin, origin + (row*height), width, height*(row+1))
            row += 1
        else:
            box = (box[0]+width, box[1], box[2]+width, box[3])

def main():
    # HOW TO USE THIS FILE
    # in word, MAKE SURE your rows are EVENLY SPACED across ALL PAGES. put a hard return in there, it helps! don't let word do them differently!
    # put all of your images in a folder that you specify in raw_dir
    # paste the kanji from your word file into raw_kanji
    # num_chars is the number of characters per page (file)
    # the template_boxes are where you want to crop the whitespace to (x1,y1,x2,y2)
    # see more instructions in make_templates()

    raw_dir = "../idk/original gothic files/oops again"

    num_chars = 64 #for mincho kanji templates, 64, for kana, 35. for small kanji, 925

    list_of_files = os.listdir(raw_dir) 
    raw_kanji = u"哺 楷 毀 賂 錮"
    kanji = raw_kanji.split()
    start = 0
    end = num_chars

    kanji_template_box_m = (125,145,1145,1305) # 1020 x 1160
    kanji_template_box_g = (117, 141, 1017, 1341) # use this one if this spaces are also in a japanese font
    kana_template_box = (95,148,1095,1198)
    sm_kanji_box = (142, 147, 1117, 1414)

    print len(kanji)

    for f in list_of_files:

        im = Image.open(raw_dir+"/"+f).convert("L")

        cropped = im.crop(kanji_template_box_g)
        # cropped.show()
        make_templates(cropped, kanji[start:end])
        start += num_chars
        end += num_chars

if __name__ == "__main__":
    main()