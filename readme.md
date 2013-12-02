# OCR-JPN

OCR-JPN is a Chrome extension that lets you recognize Japanese characters in images you find around the web. You can then copy/paste the text into your favorite dictionary, or perform a lookup on the spot using a built-in implementation of JMdict: http://www.csse.monash.edu.au/~jwb/edict_doc.html.

![demo of the OCR result]()

## Why?

The fantastic Chrome extension rikaikun https://chrome.google.com/webstore/detail/rikaikun/jipdnfibhldikgcjhfnomkfpcebammhp lets you hover over Japanese text and get a dictionary popup. However, this doesn't work on images. One way to solve this problem is to use OCR. OCR stands for Optical Character Recognition and is used to turn pictures containing representations of text into actual text that can be manipulated like text and not an image. The goal of OCR-JPN is to turn Japanese text on images into actual text so that you can look it up in a dictionary or copy/paste it into a flashcard program or notes.

## How does it work?

### OCR

Once you click on the extension icon, a dialog window will open on the current page. The window is draggable and resizeable. Draw the window over the character(s) you wish to recognize, trying to get a clean crop (although it is forgiving if you catch a little extra of the characters next to, but not above or below, your selection). Next click the camera button.

This will send a screenshot of your tab to the server. Please note that no images from your session are saved to the server. The server then crops the image and performs several manipulations using PIL (Python Imaging Library) that resizes, thresholds, and crops the image to prepare it for comparison. The program then performs an analysis to count the number of unique negative spaces present in the thresholded image and uses that as a starting point in a database of aroud 3000 Japanese characters. The script will continue to search until it finds a "good enough" score, at which point it will compare the input image to characters that have been deemed similar to the "good enough" character.

OCR-JPN works best on Gothic-type fonts (bold and blocky instead of script-like or calligraphic).

Once you get a result, you can click on each character to see the next two candidates returned from the server, in case there was a near miss.

![demo of the next two candidates]()

### The dictionary

Once you get a result back from the server, you can click the dictionary button to look up the word in the server's dictionary, which was implemented using JMdict from the University of Monash/Electronic Dictionary Research and Development Group. If the word is not in the dictionary, it will tell you. You can then copy/paste the definitions as you see fit.

![demo of the dictionary lookup]()

## Acknowledgments

Special thanks to the University of Monash/Electronic Dictionary Research and Development Group for allowing their Japanese-English dictionary JMdict to be used by the public. See the license at http://www.edrdg.org/edrdg/licence.html.

Thanks also to Hackbright Academy for outstanding mentorship. http://www.hackbrightacademy.com/