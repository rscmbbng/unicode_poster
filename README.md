# unicode_poster.py
A script that generates all Unicode code points and prints them to ``stdout``. Can be used to generate HTML pages which can be printed out into posters.
This work was made as part of Modifiying The Universal, a workshop and presentation by Femke Snelting, Peggy Pierrot & Roel Roscam Abbing during [*.exe (ver0.2)](http://softwarestudies.projects.cavi.au.dk/index.php/*.exe_%28ver0.2%29) at Malmö University.

##Usage
To print out all Unicode characters:

``./unicode_poster.py``

By default some characters are omitted because they reverse the reading direction of the characters that follow.

To print out all characters: 

``./unicode_poster.py -a``

To print out all Unicode characters and the names of each block:

``./unicode_poster.py -b``

By default the script leaves out some Unicode planes (2 SIP, PUA-A, PUA-B) because they reperesent a LOT of extra code points without glyphs

To add these extra planes anyway:

``./unicode_poster.py -e``

To print using HTML formatting:

``./unicode_poster.py -H``

The above are all combinable:

``./unicode_poster -Heab``

Download all the sources and exit the program:

``./unicode_poster.py -d``

So to make an HTML page it is sufficient to do the following:

``./unicode_postery.py -H > my_poster.html``

This repository contains a CSS file to style the resulting HTML pages. This style sheet is used to highlight all code points considered to be emoji.

##Fonts
Some fonts recommended to display as much of it as possible:

``Symbola, Aegyptus, MingLiU, Code2000, Code2001, Code2002, Musica, unifont, LastResort``

##PDF
Something along these lines worked for me on Debian:

Open the HTML page in a browser (I used Chromium).

Using the print dialog (ctrl+p) make a custom paper size, in my case 1220x5000mm @ 72dpi.

Select your custom paper size, print to file.

Now you have the PDF of Death, with embedded fonts and characters. 

Flatten it using something like Imagemagick: ``convert death.pdf flattened.pdf``
