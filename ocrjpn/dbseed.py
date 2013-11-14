import psycopg2
from PIL import Image
import os
from islands import find_islands

def main():
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    path = "../templates/kanji/mincho/"
    list_of_files = os.listdir(path)

    for i in range(len(list_of_files)):
        f = list_of_files[i]
        im = Image.open(path+f).convert("L")

        code = f.split(".")[0]
        black, white = find_islands(im)
        char_type = "kanji"
        font = "mincho"
        im_path = path + f
        jouyou = True

        cur.execute("INSERT INTO characters (code, blacks, whites, char_type, font, img_path, jouyou) VALUES (%s,%s,%s,%s,%s,%s,%s);", (code, black, white, char_type, font, im_path, jouyou))

    conn.commit()


if __name__ == "__main__":
    main()