from PIL import Image
import psycopg2
from recognize import compare_to_template

def main():
    conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
    cur = conn.cursor()

    cur.execute("SELECT code, img_path from characters where code = 24618 and font = 'gothic' and img_size='big'")
    row1 = cur.fetchone()

    cur.execute("SELECT code, img_path FROM characters where font = 'gothic' and img_size = 'big';")
    all_kanji = cur.fetchall()

    all_kanji = sorted(all_kanji, key=lambda row: row[0]) 

    test_code, test_path = row1
    test_img = Image.open(test_path).convert("L")

    f = open('similarities_24618.txt', 'w')

    for row in all_kanji:
        sim_code, img_path = row
        img = Image.open(img_path).convert("L")
        sim_score = compare_to_template(test_img, img)
        line = unichr(sim_code) + " " + str(sim_score) + "\n"
        f.write(line.encode("utf-8"))

    # for row in all_kanji:
    #     test_code, test_path = row
    #     test_img = Image.open(test_path).convert("L")
    #     for row in all_kanji:
    #         sim_code, img_path = row
    #         img = Image.open(img_path).convert("L")
    #         sim_score = compare_to_template(test_img, img)
    #         if sim_score < 0.3 and sim_score != 0:
    #             cur.execute("INSERT INTO similarities (code, similar_code, similar_code_path, score) VALUES (%s,%s,%s,%s);", (test_code, sim_code, img_path, sim_score))
    #     conn.commit()
    #     print "finished", test_code
        # line = unichr(code) + " " + str() + "\n"
        # f.write(line.encode("utf-8"))

if __name__ == "__main__":
    main()