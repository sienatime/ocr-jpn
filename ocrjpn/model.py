import psycopg2
import json
import pdb

conn = psycopg2.connect("dbname='ocrjpn' user='siena' host='localhost' password='unicorns'")
cur = conn.cursor()

def lookup(input):
    cur.execute("SELECT entries.kanji, entries.readings, senses.blob FROM entries INNER JOIN senses ON (entries.sense_id = senses.id) where entries.lookup = %s",(input,))
    rows = cur.fetchall()

    big_blob = []
    for row in rows:
        kanji, readings, blob = row
        senses = json.loads(blob)
        big_blob.append( {"entry": {"kanji":kanji, "readings":readings, "senses":senses}} )

    # pdb.set_trace()

    # ummm so I guess blob is actually a list of objects. it kind of seems like i might need to transform it back into python, just to transform it into json.

    return json.dumps(big_blob)