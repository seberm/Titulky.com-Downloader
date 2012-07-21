#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import threading
import time
from urllib import request
from urllib.parse import urlparse
from optparse import OptionParser, OptionGroup


# Globals
NAME = 'titulky_com_downloader'
PAGE = 'http://www.titulky.com'
ENCODING = 'cp1250'
CHECK_TIME = 0.05 #s

# Global variable only for now (in future it will be part of some class)
titlesLinks = []


def log(fmtstr):
    print(fmtstr)


class IFrameParser(threading.Thread):

    def __init__(self, url, name, encoding):
        self.__url = url
        self.__name = name
        self.__encoding = encoding

        threading.Thread.__init__(self)


    def run(self):
         
        fd = request.urlopen(self.__url)
        iframe = str(fd.read().decode(self.__encoding))
        fd.close()

        #pattern = r'<a[\s]+[^h]+href="(?P<addr>[^"]+)"[^>]*>'
        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        data = re.search(pattern, iframe, re.VERBOSE)

        if data:
            #log('%s: %s' % (self.__name, PAGE + data.group('addr')))
            titlesLinks.append((self.__name, PAGE + data.group('addr')))
        else:
          #<img src="./captcha/captcha.php" />
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                log('%s: You exhausted your daily limit of downloads' % self.__name)
            else:
                log('%s: Cannot find data on page' % self.__name)



def getLinks(url, encoding):

    fd = request.urlopen(url.geturl())
    htmlSource = str(fd.read().decode(encoding))
    fd.close()

    pattern = r'''
            <a                                           # Tag start
            [\s]+                                        # Ignore white chars
            class="titulkydownloadajax[^"]*"             # Find right html tag
            [\s]+
            href="(?P<addr>[^"]+)"[^>]*                  # Find address in href (addr)
            >
            (?P<name>[^<]*)                              # Find name of movie (name)
            </a>                                         # Tag end
           '''

    links = re.findall(pattern, htmlSource, re.VERBOSE)

    if links:
        for link in links:

            iframeURL = PAGE + '/' + link[0]
            name = link[1]

            # Start thread
            IFrameParser(iframeURL, name, encoding).start()

        # We're active waiting for end of all threads
        # @todo Completely rewrite this
        while threading.active_count() != 1:
            time.sleep(CHECK_TIME)

        return titlesLinks
    else:
        log('Cannot find data on page')
        sys.exit(1)


def downloadFiles(links = []):

    # @todo It's neccessary to use urllib2! But it's not working for me
    for name, url in links:
        fd = request.urlopen(url)
        titles = open(name, 'wb')
        titles.write(fd.read())
        titles.close()


def main():

    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [options]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)')

    options = OptionGroup(parser, 'Program Options', 'Options specific to titulky_com_downloader.')
    
    options.add_option('-l', '--link', dest='link', action='store_true', help='Prints download link on stdout (default behaviour)')
    options.add_option('-e', '--encoding', dest='encoding', action='store', metavar='<encoding>', default=ENCODING, help='Sets webpage encoding default [cp1250]')
    options.add_option('-n', '--with-name', dest='withName', action='store_true', help='Prints download links with their name')
    options.add_option('-d', '--download', dest='download', action='store_true', help='Download subtitles')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()

    if not args[0:]:
        log('You have to provide an URL address!')
        sys.exit(1)

    for arg in args:
        url = urlparse(arg)

        links = getLinks(url, opt.encoding)

        if opt.download:
            downloadFiles(links)

        if opt.withName:
            for l in links:
                log('%s: %s' % (l[0], l[1]))
        else:
            for l in links:
                log(l[1])



if __name__ == '__main__':
    main()
