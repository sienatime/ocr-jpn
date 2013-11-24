# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import codecs
import psycopg2
import pdb

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

def no_tag_concat(list_tags):
    for i in range(len(list_tags)):
        list_tags[i] = list_tags[i].get_text()

    return ", ".join(list_tags)

def main():
    f = codecs.open("../kanjidic/test.xml", encoding='utf-8')
    text = f.read()

    soup = BeautifulSoup(text)

    # returns list of entries
    entries = soup.find_all('entry')

    counter = 0
    for entry in entries:
        counter += 1
        keb = None  
        if entry.keb:
            keb = entry.find('keb').get_text()

        taggy_rebs = entry.find_all('reb')

        rebs = no_tag_concat(taggy_rebs)

        cur.execute("INSERT INTO entries (keb, reb) VALUES (%s, %s) RETURNING id;",(keb, rebs))
        entry_id = cur.fetchone()[0]

        senses = entry.find_all('sense')

        for sense in senses:
            parts_of_speech = None
            if sense.pos:
                parts_of_speech = no_tag_concat(sense.find_all('pos'))
            misc = None
            if sense.misc:
                misc = sense.misc.get_text()

            cur.execute("INSERT INTO senses (entry_id, parts_of_speech, misc) VALUES (%s, %s, %s) RETURNING id;",(entry_id, parts_of_speech, misc))
            sense_id = cur.fetchone()[0]

            # glosses = sense.find_all(attrs={"xml:lang": "dut"})
            glosses = sense.find_all('gloss')

            if len(glosses) == 0:
                pdb.set_trace()

            for gloss in glosses:
                # pdb.set_trace()
                definition = gloss.get_text()

                lang = gloss.attrs.get('xml:lang')

                if lang == 'dut':
                    lang = 'nl'
                elif lang == 'ger':
                    lang = 'de'
                elif lang == 'fre':
                    lang = 'fr'
                elif lang == 'rus':
                    lang = 'ru'
                else:
                    lang = "en"

                cur.execute("INSERT INTO glosses (sense_id, definition, lang) VALUES (%s, %s, %s);",(sense_id, definition, lang))
        
        if counter % 100 == 0:
            print "commting", counter    
            conn.commit()

    # try inserting this into db

    # 3 tables: entries, senses, glosses
    # an entry can have many senses
    # entry's reb (reading) can have many so let's just concatenate those too
    # a sense can have many glosses

    # concatenate pos (parts of speech) together because we don't care

    # WATCH OUT for unicode




main()