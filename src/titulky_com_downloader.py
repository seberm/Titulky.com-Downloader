#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import threading
import time
from urllib import request
from urllib.parse import urlparse, urlencode
from http import cookiejar
from optparse import OptionParser, OptionGroup


# Globals
NAME = 'titulky_com_downloader'
VERSION = '1.0.0-beta'

PAGE = 'http://www.titulky.com'

# For debugging
#PAGE = 'http://localhost/downloader-titulky_com'

PAGE_ENCODING = 'cp1250'
CHECK_TIME = 0.05 #s

# Global variable only for now (in future it will be part of some class)
titlesLinks = []


def log(fmtstr):
    print(fmtstr)


class IFrameParser(threading.Thread):

    def __init__(self, opener, url, name, encoding):

        self.__opener = opener
        self.__url = url
        self.__name = name
        self.__encoding = encoding

        threading.Thread.__init__(self)


    def run(self):
         
        fd = self.__opener.open(self.__url)
        iframe = str(fd.read().decode(self.__encoding))
#fd.close()?

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
            titlesLinks.append((self.__name, PAGE + data.group('addr')))
        else:
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                log('%s: You exhausted your free daily limit of downloads - it\'s necessary to re-type captcha code' % self.__name)
            else:
                log('%s: Cannot find data on page' % self.__name)



def getLinks(url, encoding, login, password):

    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    
    loginData = urlencode({'Login' : login, 'Password' : password, 'foreverlog' : 1})

    # We send POST data to login
    if login and password:
        opener.open('http://www.titulky.com/index.php', loginData.encode(encoding))

    fd = opener.open(url.geturl())
    htmlSource = str(fd.read().decode(encoding))
#fd.close()?

    pattern = r'''
            <td                                         # TD before hyperlink (it's because program downloaded all titles including titles from history box
            [\s]+
            class="detailv"
            [\s]*
            >
            [\s]*
            <a                                           # Tag start
            [\s]+                                        # Ignore white chars
            class="titulkydownloadajax"                  # Find right html tag
            [\s]+
            href="(?P<addr>[^"]+)"                       # Find address in href (addr)
            [\s]*
            [^>]*>
            (?P<name>[^<]*)                              # Find name of movie (name)
            </a>                                         # Tag end
           '''

    links = re.findall(pattern, htmlSource, re.VERBOSE)

    if links:
        for link in links:

            iframeURL = PAGE + '/' + link[0]
            name = link[1]

            # Start thread
            IFrameParser(opener, iframeURL, name, encoding).start()

        # We're active waiting for end of all threads
        # @todo Completely rewrite this
        while threading.active_count() != 1:
            time.sleep(CHECK_TIME)

        return titlesLinks
    else:
        log('Cannot find data on page')
        sys.exit(1)


def downloadFiles(links = []):

    for name, url in links:
        
        # I don't know why but it's necessary to slow down next downlad of titles
        # @todo Some better solution or workaround?
        time.sleep(1.0)

        fd = request.urlopen(url)

        with open(name + '.srt', mode='wb') as titles:
            titles.write(fd.read())

        fd.close()


def main():

    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [options]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)',
                          version = '%prog ' + VERSION)

    options = OptionGroup(parser, 'Program Options', 'Options specific to titulky_com_downloader.')
    
    options.add_option('-l', '--link', dest='link', action='store_true', help='Print download link(s) on stdout (default behaviour)')
    options.add_option('-e', '--page-encoding', dest='pageEncoding', action='store', metavar='<encoding>', default=PAGE_ENCODING, help='Sets webpage encoding - default [cp1250]')
    options.add_option('-n', '--with-name', dest='withName', action='store_true', help='Print download links with movie name')
    options.add_option('-p', '--dir', dest='dir', action='store', help='Change program directory')
    options.add_option('--login', dest='login', action='store', default='', help='Login name to netusers.cz (titulky.com)')
    options.add_option('--password', dest='password', action='store', default='', help='Password to netusers.cz (titulky.com)')

    # @todo Remove warning message in following option
    options.add_option('-d', '--download', dest='download', action='store_true', help='Download subtitles to current folder (sometimes does not work - use option -l in combination with wget - just take a look to README)')

    # @todo it will be possible to add prefix to downloaded files
    #options.add_option('--prefix', dest='prefix', action='store_true', help='Set prefix to downloaded files')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()

    if not args[0:]:
        log('You have to provide an URL address!')
        sys.exit(1)

    for arg in args:
        url = urlparse(arg)

        links = getLinks(url, opt.pageEncoding, opt.login, opt.password)

        if opt.dir:
            os.chdir(opt.dir)

        if opt.download:
            downloadFiles(links)

        if opt.withName:
            for l in links:
                log('%s: %s' % (l[0], l[1]))
        elif not opt.download:
            for l in links:
                log(l[1])



if __name__ == '__main__':
    main()
