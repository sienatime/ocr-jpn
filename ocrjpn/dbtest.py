from PIL import Image
from recognize import process_image, split_images, compare_to_template
from islands import find_islands
import psycopg2
from sys import argv
import os

if len(argv) == 3:
    script, img, mode = argv

def run_thru_templates(im):
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    im_black, im_white = find_islands(im)
    cur.execute("SELECT code, img_path from characters where blacks = %s and whites = %s;", (im_black, im_white))
    matches = cur.fetchall()

    scores = []
    for row in matches:
        code, img_path = row
        template = Image.open(img_path).convert("L")
        scores.append( (code, compare_to_template(im, template)) )

    return scores

def move_files():
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()
    cur.execute("SELECT code, font, img_path from characters where char_type = 'kanji' and img_path like '%mincho/%' and jouyou = False;")

    rows = cur.fetchall()

    for row in rows:
        code, font, img_path = row
        print img_path
        tokens = img_path.split("mincho/")
        print tokens
        new_path = tokens[0] + "mincho extra/" + tokens[1]
        cur.execute("UPDATE characters SET img_path = %s WHERE code = %s AND font = %s;", (new_path, code, font))

    conn.commit()


def update_paths():
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    cur.execute("SELECT code, font, img_path from characters WHERE jouyou = True and img_path like '%mincho extra%';")
    rows = cur.fetchall()

    for row in rows:
        code, font, old_path = row
        tokens = old_path.split(" extra")
        new_path = tokens[0] + tokens[1]
        print new_path
        cur.execute("UPDATE characters set img_path = %s where code = %s and font = %s;", (new_path, code, font))

    conn.commit()

def parse_score(score):
    # score is a tuple constructed like (filename.bmp, score)
    return unichr(score[0])

def main():
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

if __name__ == "__main__":
    main()