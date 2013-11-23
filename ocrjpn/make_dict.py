# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import codecs
import psycopg2

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

def main():
    f = codecs.open("../kanjidic/test.xml", encoding='utf-8')
    text = f.read()

    soup = BeautifulSoup(text)

    # returns list of entries
    entries = soup.find_all('entry')
    for entry in entries:
        print "new entry"
        keb = None  
        if entry.keb:
            keb = entry.find('keb').get_text()
            print "keb", keb
        else:
            print "no keb"
        taggy_rebs = entry.find_all('reb')

        rebs = ""
        for i in range(len(taggy_rebs)):
            taggy_rebs[i] = taggy_rebs[i].get_text()

        rebs = ", ".join(taggy_rebs)
        print rebs

        cur.execute("INSERT INTO entries (keb, reb) VALUES (%s, %s);",(keb, rebs))
    
    conn.commit()

    # try inserting this into db

    # 3 tables: entries, senses, glosses
    # an entry can have many senses
    # entry's reb (reading) can have many so let's just concatenate those too
    # a sense can have many glosses

    # concatenate pos (parts of speech) together because we don't care

    # WATCH OUT for unicode




main()