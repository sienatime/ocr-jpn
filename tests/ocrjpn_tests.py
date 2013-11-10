# -*- coding: utf-8 -*-
from nose.tools import *
from ocrjpn import recognize
from PIL import Image
import os

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_simple_islands():
    isl = open_image("isl.bmp")
    assert_equal( recognize.find_islands(isl), (2, 2) )
    isl2 = open_image("isl2.bmp")
    assert_equal( recognize.find_islands(isl2), (3, 1) )
    perp = open_image("perp.bmp")
    assert_equal( recognize.find_islands(perp), (1, 2) )

def test_simple_radicals():
    hitoben = open_image("hitoben.bmp")
    assert_equal( recognize.find_islands(hitoben), (1, 3) )
    lid = open_image("lid.bmp")
    assert_equal( recognize.find_islands(lid), (1, 2) )
    i1 = open_image("i1.bmp")
    assert_equal( recognize.find_islands(i1), (1, 2) )
    i3 = open_image("i3.bmp")
    assert_equal( recognize.find_islands(i3), (1, 2) )
    i4 = open_image("i4.bmp")
    assert_equal( recognize.find_islands(i4), (1, 2) )
    i5 = open_image("i5.bmp")
    assert_equal( recognize.find_islands(i5), (1, 2) )

def test_sm_kanji():
    smtada = open_template("smtada.bmp")
    assert_equal( recognize.find_islands(smtada), (3, 5) )

    smi = open_template("smi.bmp")
    assert_equal( recognize.find_islands(smi), (4, 3) )

def test_big_kanji():
    list_of_files = os.listdir("templates/test/")

    tada = open_template(list_of_files[2])
    assert_equal( recognize.find_islands(tada), (3, 5) )

    i = open_template(list_of_files[3])
    assert_equal( recognize.find_islands(i), (4, 3) )

def open_image(str):
    path = "test_images/" + str
    return Image.open(path).convert("L")

def open_template(str):
    path = "templates/test/" + str
    return Image.open(path).convert("L")