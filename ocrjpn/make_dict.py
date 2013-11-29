# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import codecs
import psycopg2
import pdb
import json

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

def no_tag_concat(list_tags):
    for i in range(len(list_tags)):
        list_tags[i] = list_tags[i].get_text()

    return ", ".join(list_tags)

def main():
    f = codecs.open("../kanjidic/JMdict", encoding='utf-8')
    print "opened file"
    text = f.readlines()
    print "read file"

    # soup = BeautifulSoup(text)
    print "made soup"

    
    start = None

    counter = 0

    for i in range(3898731, len(text)):
        if "<entry>" in text[i]:

            start = i
        elif "</entry>" in text[i]:
            end = i

            entry_list = text[start:end+1]
            entry_string = ""
            for elt in entry_list:
                entry_string += elt.strip()

            #process stuff
            soup = BeautifulSoup(entry_string)

            entry = soup.entry

            counter += 1
            # maybe do the sense blob first so you can get the ID, the make as many entries rows as needed.
            # find all kebs and rebs and make them unique lookup rows.
            senses = entry.find_all('sense')
            senses_blob = []

            for sense in senses:
                # make a JSON blob with the following structure
                # senses is a list of objects
                #   the objects can optionally have a list of parts_of_speech
                #   optionally have list of misc
                #   MUST have glosses obj where the keys are languages and the values are lists of strings
                parts_of_speech = None
                if sense.pos:
                    parts_of_speech = [pos.get_text() for pos in sense.find_all('pos')]

                misc = None
                if sense.misc:
                    misc = [misc.get_text() for misc in sense.find_all('misc')]

                glosses = sense.find_all('gloss')
                english = []
                french = []
                german = []
                dutch = []
                russian = []

                for gloss in glosses:
                    # pdb.set_trace()
                    definition = gloss.get_text()

                    lang = gloss.attrs.get('xml:lang')

                    if lang == 'dut':
                        dutch.append(definition)
                    elif lang == 'ger':
                        german.append(definition)
                    elif lang == 'fre':
                        french.append(definition)
                    elif lang == 'rus':
                        russian.append(definition)
                    else:
                        english.append(definition)

                blob = {"glosses": {"en" : english, "nl" : dutch, "de" : german, "ru" : russian, "fr" : french}, "pos" : parts_of_speech, "misc" : misc}
                senses_blob.append(blob)

            cur.execute("INSERT INTO senses (blob) VALUES (%s) RETURNING id;",(json.dumps(senses_blob),))
            sense_id = cur.fetchone()[0]

            lookup = []
            rebs = [reb.get_text() for reb in entry.find_all('reb')]

            str_kanji = None
            if entry.keb:
                kebs = [keb.get_text() for keb in entry.find_all('keb')]
                str_kanji = ", ".join(kebs)
                lookup += kebs

            lookup += rebs
            
            str_readings = ", ".join(rebs)

            for term in lookup:
                cur.execute("INSERT INTO entries (lookup, kanji, readings, sense_id) VALUES (%s, %s, %s, %s)",(term, str_kanji, str_readings, sense_id))

            if counter % 1000 == 0:
                print "committing", counter
                conn.commit()

    conn.commit()

main()