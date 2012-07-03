#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys
import urllib.request 

if sys.argv[1:]:
    url = sys.argv[1:][0]
else:
    print('You must provide URL adress')
    sys.exit(1)


# Ziskame stranku
fd = urllib.request.urlopen(url)
htmlSource = str(fd.read().decode('cp1250'))
fd.close()


# z tohoto ziskame adresu href..., a jeji cilovou stranku stahneme do tmp...a znovu rozparsujeme


#<a[^>]+id="bleh"[^>]+href="([^"]+)"[^>]*>
#pattern = r'<a[\s]+class="titulkydownloadajax[\s]cboxElement"[\s]+href="(.*?)"' #funguje
#pattern = r'<a[\s]+class="titulkydownloadajax"[\s]+href="(.*?)"'

pattern = r'''
            <a
            [\s]+                            # Ignorujeme bile znaky
            class="titulkydownloadajax"      # Najdeme spravny HTML prvek
            [\s]+
            href="(?P<addr>[^"]+)"[^>]*      # Najdeme adresu, ktera je v href="..." a pojmenujeme si ji 'addr'
            >
            (?P<name>[^<]*)</a>              # Ulozime si i nazev filmu / serialu, pro ktery titulky stahujeme 'name'
           '''

data = re.search(pattern, htmlSource, re.VERBOSE)

if data:
    link = 'http://www.titulky.com/' + data.group('addr')
    name = data.group('name')

    #print('Adresa iframe:', link)
    #print('Jmeno serialu/filmu:', name)

    fd = urllib.request.urlopen(link)
    iframe = str(fd.read().decode('cp1250'))
    fd.close()

    pattern = r'<a[\s]+[^h]+href="(?P<addr>[^"]+)"[^>]*>'
    data = re.search(pattern, iframe, re.VERBOSE)
    resLink = 'http://www.titulky.com' + data.group('addr')

    # Vytiskneme link na stdout
    print(resLink)

else: print('No data found')

