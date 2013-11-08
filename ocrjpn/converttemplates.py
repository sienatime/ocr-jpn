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
    width = 200 #125 for kanji
    height = 150 #145 for kanji
    origin = 0
    box = (0, 0, width, height)
    row = 1

    for i in range(1, len(kanji)+1):
        print i
        print box
        work = im.crop(box)

        new_image, black_pixels = threshold_image(work)
        new_work = crop_image(new_image, black_pixels)
        save_image(new_work, kanji[i-1]+".bmp", "BMP")

        if i % 5 == 0 and i != 0: #8 for kanji
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

    raw_dir = "../idk/original mincho files/katakana"

    num_chars = 35 #for kanji templates, 64

    list_of_files = os.listdir(raw_dir) 
    raw_kanji = u"ア　イ　ウ　エ　オ カ　キ　ク　ケ　コ サ　シ　ス　セ　ソ タ　チ　ツ　テ　ト ナ　ニ　ヌ　ネ　ノ ハ　ヒ　フ　ヘ　ホ マ　ミ　ム　メ　モ ラ　リ　ル　レ　ロ ワ　ヲ　ン　ガ　ギ グ　ゲ　ゴ　ザ　ジ ズ　ゼ　ゾ　ダ　ヂ ヅ　デ　ド　バ　ビ ブ　ベ　ボ　パ　ピ　プ　ペ　ポ　ヤ　ユ ヨ　ヱ　ヰ"
    kanji = raw_kanji.split()
    start = 0
    end = num_chars

    kanji_template_box = (125,145,1145,1305)
    kana_template_box = (95,148,1095,1198)

    print len(kanji)

    for f in list_of_files:

        im = Image.open(raw_dir+"/"+f).convert("L")

        cropped = im.crop(kana_template_box)
        make_templates(cropped, kanji[start:end])
        start += num_chars
        end += num_chars

if __name__ == "__main__":
    main()