from PIL import Image
from recognize import process_image, split_images, compare_to_template
from islands import find_islands
import psycopg2
from sys import argv

if len(argv) == 3:
    script, img, mode = argv

def run_thru_templates(im):
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    im_black, im_white = find_islands(im)
    # query = "SELECT * from characters where blacks = %s and whites = %s;", (im_black, im_white)
    cur.execute("SELECT code, img_path from characters where blacks = %s and whites = %s;", (im_black, im_white))
    matches = cur.fetchall()

    scores = []
    for row in matches:
        code, img_path = row
        template = Image.open(img_path).convert("L")
        scores.append( (code, compare_to_template(im, template)) )

    return scores

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