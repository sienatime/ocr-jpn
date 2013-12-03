# -*- coding: utf-8 -*-
from nose.tools import *
from ocrjpn import recognize
from PIL import Image
import os

def ocr(image_name):
    results = recognize.ocr_image(open_image(image_name))
    
    final_answer = ""
    for result in results:
        final_answer += result[0]
    return final_answer

def test_nihon():
    assert_equal(ocr("nihon.bmp"), u"日本")

def test_asahi():
    assert_equal(ocr("asahishinbun3.bmp"), u"朝日新聞")

def test_daigaku():
    assert_equal(ocr("daigaku.bmp"), u"大学")

def test_jouchi():
    assert_equal(ocr("jouchiclean.bmp"), u"上智")

def test_kaigaishucchou():
    assert_equal(ocr("yoji.bmp"), u"海外出張")

def open_image(image_name):
    base_path = "../test_images/"
    return Image.open(base_path + image_name)