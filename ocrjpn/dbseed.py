import psycopg2
from PIL import Image
import os
from islands import find_islands

CONN = None
CUR = None

def add_columns():
    CUR.execute("SELECT code, whites from characters WHERE font = 'gothic' and img_size = 'small';")
    small_rows = CUR.fetchall()

    for row in small_rows:
        code, whites = row
        CUR.execute("UPDATE characters set sm_whites = %s where font = %s img_size = %s and code = %s;",(whites, 'gothic', 'big', code))

def insert_from_list(path, list_of_files):
    global CUR
    if "mincho" in path:
        font = "mincho"
    elif "gothic" in path:
        font = "gothic"

    for i in range(len(list_of_files)):
        f = list_of_files[i]
        im = Image.open(path+f).convert("L")

        code = f.split(".")[0]
        black, white = find_islands(im)
        char_type = "kanji"
        im_path = path + f
        jouyou = True
        size = 'small'

        CUR.execute("INSERT INTO characters (code, blacks, whites, char_type, font, img_path, jouyou, img_size) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", (code, black, white, char_type, font, im_path, jouyou, size))

def main():
    global CONN
    global CUR
    CONN = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    CUR = CONN.cursor()

    # path = "../templates/kanji/small mincho/"
    # list_of_files = os.listdir(path)

    # insert_from_list(path, list_of_files)

    add_columns()

    CONN.commit()


if __name__ == "__main__":
    main()