# -*- coding: utf-8 -*-
import psycopg2

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

def main():
    cur.execute("SELECT entries.kanji, entries.readings, senses.blob FROM entries INNER JOIN senses ON (entries.sense_id = senses.id) where entries.lookup = %s",(u'さびしい',))
    test = cur.fetchone()

    kanji, readings, blob = test

    print blob

main()