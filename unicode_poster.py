#!/usr/bin/env python

# unicode_poster.py
# A script that generates all Unicode code points and prints them stdout. Can be used to generate HTML pages which can be printed out into posters.
# Some fonts recommended to display as much of it as possible: Symbola, Aegyptus, MingLiU, Code2000, Code2001, Code2002, Musica, unifont, LastResort

# Usage:
#     To print out all Unicode characters:
#    ./unicode_poster.py

#     By default some characters are omitted because they reverse the reading direction of the characters that come after
#     To print out all characters: 
#    ./unicode_poster.py -a

#     To print out all Unicode characters and the names of each block:
#    ./unicode_poster.py -b

#     By default the script leaves out some Unicode planes (2 SIP, PUA-A, PUA-B) because they reperesent a lot of extra code points without glyphs
#     To add these extra planes anyway:
#     ./unicode_poster.py -e

#     To print using HTML formatting:
#     ./unicode_poster.py -H

#     The above are all combinable:
#     ./unicode_poster -Heab

#     Download all the sources and exit the program:
#     ./unicode_poster.py -d

#     So to make an HTML page it is sufficient to do the following:
#     ./unicode_postery.py -H > 

# GPL3
# Roel Roscam Abbing 2016, http://roelof.info
# Created for a presentation and workshop at: http://softwarestudies.projects.cavi.au.dk/index.php/*.exe_%28ver0.2%29

import re, urllib2, os, argparse
def get_unicode_blocks():
    #turns output from http://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt
    #into a dictionary of unicode block names with corresponding number ranges and writes them to a file.
    import urllib2, os

    if not os.path.isfile('Blocks.txt'):
        with open('Blocks.txt', 'wb') as f:
            ublocks = urllib2.urlopen('http://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt').read()
            f.write(ublocks)
            print ('Downloaded Unicode Blocks list and wrote to blocks.txt')
            ublocks = ublocks.split('\n')

    else:
        #print ('Reading unicode blocks from file')
        ublocks = open('Blocks.txt').readlines()

    b = {}

    for i in ublocks:
        if not i.startswith('#') and not i.startswith('\n') and not len(i)==0:
            i=i.strip('\n')
            i=i.split('; ')
            ranges = i[0].split('..')
            block_name = i[1]
            b[block_name] = int(ranges[0],16), int(ranges[1],16) #turn each string in list into tuple w/ base 16 integers

    return b


def identify_emoji():
    #use http://www.unicode.org/Public/emoji/2.0//emoji-data.txt
    #as a source to determine which unicode points are considered emojiex
    #returns a list of integers

    import urllib2, os, re

    if not os.path.isfile('emoji_list.txt'):
        with open('emoji_list.txt', 'wb') as f:
            if not os.path.isfile('emoji-data.txt'):
                latest_emoji_data=urllib2.urlopen('http://www.unicode.org/Public/emoji/latest/emoji-data.txt').geturl()
                emojilist = urllib2.urlopen(latest_emoji_data).read()
                print ('Downloaded Unicode list of emojis and wrote them to emoji-list.txt')
            else: 
                emojilist = open('emoji-data.txt').read()#.split('\n')
            f.write(emojilist)
    else:
        #print ('Reading emoji from file')
        emojilist = open('emoji_list.txt').read()


    emoji_numbers = []
    t = []
    for i in emojilist.split('\n'):
        if not i.startswith('#'):
            if not i.startswith('\n'):
                if not len(i)==0:

                    i=i.strip('\n')
                    i=i.split('; ')
                    ranges = i[0].split('..')

                    if len(ranges) < 2:
                        emoji_numbers.append(int(ranges[0],16))
                    else:
                        for num in range(int(ranges[0],16), int(ranges[1],16)):
                            emoji_numbers.append(num)

    return set(emoji_numbers)

def get_exceptions():
    #we don't want all characters in the poster because they will mess it up.
    #think of characters that change the writing direction:
    #https://en.wikipedia.org/wiki/General_Punctuation_(Unicode_block)
    
    exceptions = [int(0x205F)]
    for i in range(int(0x2000),int(0x200F)):
        exceptions.append(i)
    for i in range(int(0x2028),int(0x202F)):
        exceptions.append(i)
    for i in range(int(0x2066),int(0x206F)):
        exceptions.append(i)

    return exceptions

def extended():
    #More unicode tables! Enabling these will add another 184,000 codepoints. Most of which don't have glyphs. Up to you..
    #Tweak this function to fine tune what you include or not.

    PUA=['Tags','Supplementary Private Use Area-A', 'Supplementary Private Use Area-B']
    CJK_Extensions= ['CJK Unified Ideographs Extension B', 'CJK Unified Ideographs Extension C', 'CJK Unified Ideographs Extension D',
    'CJK Unified Ideographs Extension E']

    extended=[]
    for i in PUA:
        extended.append(i)
    for i in CJK_Extensions:
        extended.append(i)

    return extended

def download():
    print "Downlading source files, this might take a while and won't show any progress"

    try:
        os.system('rm Blocks.txt emoji_list.txt')
    except:
        pass

    a = identify_emoji()
    b = get_unicode_blocks()

    if a and b:
        print'Done downloading'
        quit()
    else:
        print "Didn't manage to download everything, try running the script with the -d flag again"
        quit()


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', help="Prints out ALL Unicode characters, which will cause trouble like mirroring characters etc.", action="store_true")
parser.add_argument('-b', '--block', help="Print as blocks with block names (e.g. 'Latin-A').", action="store_true")
parser.add_argument('-d', '--download', help="Downloads source files and exits the program.", action="store_true")
parser.add_argument('-e', '--extended', help="Print the extended Unicode tables (SIP, SSP, PUA-A/B)", action="store_true")
parser.add_argument('-H','--html', help="Print with HTML formatting, otherwise will produce plain text.", action="store_true")

#not yet implemented, nor planning to do so any time soon
#parser.add_argument('-l', '--legend', help="Add a legend (requires colors).", action="store_true")
#parser.add_argument('-c' ,'--color', help="Enable colors.", action="store_true")

args = parser.parse_args()

if args.download:
    download()

emoji_numbers = identify_emoji()

if args.html:

    print """

    <head>
    <meta charset="UTF-8">
    <link href="style.css" type="text/css" rel="stylesheet">
    </head> 

    """
    print '<center><H1><b><u>The Unicode Table</b></u></H1>'
    print '<h3>AN OVERVIEW OF MOST VISIBLE AND INVISIBLE CODE-POINTS IN THE UNICODE 8.0 BASIC AND SUPPLEMENTARY MULTILINGUAL PLANES </h3></center>'

blocks = get_unicode_blocks()
#swap the keys and values so we can lookup by number range later
rev_blocks= dict((v,k) for k,v in blocks.iteritems())

#blocks by number
bbn = blocks.values()
bbn.sort()

exceptions = get_exceptions()

extended = extended()

for block_range in bbn:
    if args.html:
        print '<span class="block" id="'+rev_blocks[block_range].replace(' ','_')+'">'
        
    if args.block:
            if rev_blocks[block_range] in extended:
                if args.extended and args.html:
                    print '<div class="block_header">',rev_blocks[block_range],'</div>'
                if args.extended:
                    print rev_blocks[block_range]
            else: 
                if args.html:
                   print '<div class="block_header">',rev_blocks[block_range],'</div>'
                else:
                    print rev_blocks[block_range]

    #block range unpacked from (0000,000F) to [0000, 0001, 0002, 0003 etc...0000F]
    bru = range(int(block_range[0]), int(block_range[1]))

    for character in bru:

        if not args.all:
            if 'Private Use Area' in rev_blocks[block_range]:
                character = 58582 #ugly shit but I can't generate empty PUA otherwise
            if character in exceptions:
                break
        if not args.extended:
            if rev_blocks[block_range] in extended:
                break

        for memory_point in emoji_numbers:
            if character == memory_point:
                if args.html:
                    print '<span class="emoji">',unichr(character).encode('UTF-8'),'</span>'
                    break
                else:
                    print unichr(character).encode('UTF-8')
                    break

        else:
            print unichr(character).encode('UTF-8')
        

    if args.html:
        print '</span>'
