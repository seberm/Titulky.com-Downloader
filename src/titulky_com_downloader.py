#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import threading
import logging
import time
import urllib
from urllib import request
from urllib.parse import urlparse, urlencode
from http import cookiejar
from optparse import OptionParser, OptionGroup


# Globals
NAME = 'titulky_com_downloader'
VERSION = '1.0.0-beta'

PAGE = 'http://www.titulky.com'

DEFAULT_LOGGING_LEVEL = 'INFO' #logging.INFO
DEFAULT_LOGGING_FORMAT = '%(levelname)s: %(message)s'

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

        logging.debug('[%s]: Running new IFrameParser thread (%s)' % (self.__name, self.__url))
         
        try:
            fd = self.__opener.open(self.__url)
            iframe = str(fd.read().decode(self.__encoding))
        except urllib.error.URLError as e:
            logging.error('[%s]: URL error: %s' % (self.__name, e.reason))
        except IOError:
            logging.error('[%s]: IO Error - thread exiting' % self.__name)
            fd.close()
            sys.exit(1)

        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        logging.debug('[%s]: Parsing iframe ...' % self.__name)

        data = re.search(pattern, iframe, re.VERBOSE)

        if data:
            logging.debug('[%s]: Found link: %s' % (self.__name, PAGE + data.group('addr')))
            titlesLinks.append((self.__name, PAGE + data.group('addr')))
        else:
            logging.debug('[%s]: No links found' % self.__name)
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                logging.warning('[%s]: You exhausted your free daily limit of downloads - it\'s necessary to re-type captcha code' % self.__name)
            else:
                logging.info('[%s]: Cannot find data on page' % self.__name)



def getLinks(url, encoding, login, password):

    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    
    loginData = urlencode({'Login' : login, 'Password' : password, 'foreverlog' : 1})

    htmlSource = ''

    try:
        # We send POST data to login
        if login and password:
            logging.debug('Posting login credentials [user: %s]' % login)
            opener.open('http://www.titulky.com/index.php', loginData.encode(encoding))

        fd = opener.open(url.geturl())

        htmlSource = str(fd.read().decode(encoding))

    except urllib.error.HTTPError as e:
        log('HTTP Connection error (%d): %s' % (e.code, e.reason))
        sys.exit(1)
    except urllib.error.URLError as e:
        logging.error('URL error: %s' % e.reason)
        sys.exit(1)
    except IOError:
        logging.error('Cannot read page data - %s' % url)
        sys.exit(1)
    except ValueError:
        logging.error('URL value error: Unknown URL type')
        sys.exit(1)

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

    logging.debug('Looking for subtitles links on %s' % url.geturl())

    links = re.findall(pattern, htmlSource, re.VERBOSE)

    if links:
        logging.debug('Links found: %d' % len(links))
        for link in links:

            iframeURL = PAGE + '/' + link[0]
            name = link[1]

            try:
                # Start thread
                IFrameParser(opener, iframeURL, name, encoding).start()
            except RuntimeError as e:
                logging.exception('Runtime error: %s' % e)
                sys.exit(1)

        # We're active waiting for end of all threads
        # @todo Some better solution or workaround?
        # @todo Completely rewrite this
        while threading.active_count() != 1:
            time.sleep(CHECK_TIME)

        return titlesLinks
    else:
        logging.info('Cannot find data on page')
        sys.exit(1)


def downloadFiles(links = []):

    logging.debug('Downloading links: %d' % len(links))

    for name, url in links:

        try:
            logging.debug('[%s]: Downloading from: %s' % (name, url))
            fd = request.urlopen(url)

            with open(name + '.srt', mode='wb') as titles:
                titles.write(fd.read())

            fd.close()
        except urllib.error.URLError as e:
            logging.error('[%s]: Cannot get subtitles: %s' % (name, e.reason))
            sys.exit(1)
        except IOError:
            logging.error('[%s]: Cannot open file: %s.srt' % (name, name))
            sys.exit(1)


def main():

    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [OPTION]... [URL]...',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)',
                          version = '%prog ' + VERSION)

    options = OptionGroup(parser, 'Program Options', 'Options specific to titulky_com_downloader.')
    
    options.add_option('-l', '--link', dest='link', action='store_true', help='Print download link(s) on stdout (default behaviour)')
    options.add_option('-e', '--page-encoding', dest='pageEncoding', action='store', metavar='<encoding>', default=PAGE_ENCODING, help='Sets webpage encoding - default [cp1250]')
    options.add_option('-n', '--with-name', dest='withName', action='store_true', help='Print download links with movie name')
    options.add_option('-p', '--dir', dest='dir', action='store', help='Change program directory')
    options.add_option('--login', dest='login', action='store', default='', help='Login name to netusers.cz (titulky.com)')
    options.add_option('--password', dest='password', action='store', default='', help='Password to netusers.cz (titulky.com)')
    options.add_option('--log', dest='logLevel', action='store', default=DEFAULT_LOGGING_LEVEL, help='Set logging level (debug, info, warning, error, critical)')

    # @todo Remove warning message in following option
    options.add_option('-d', '--download', dest='download', action='store_true', help='Download subtitles to current folder (sometimes does not work - use option -l in combination with wget - just take a look to README)')

    # @todo it will be possible to add prefix to downloaded files
    #options.add_option('--prefix', dest='prefix', action='store_true', help='Set prefix to downloaded files')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()

    level = DEFAULT_LOGGING_LEVEL
    if opt.logLevel:
        level = opt.logLevel

    try:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=level.upper())
    except ValueError:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=DEFAULT_LOGGING_LEVEL)
        logging.warning('It is not possible to set logging level to %s' % level)
        logging.warning('Using default setting logging level: INFO')

    if opt.dir:
        logging.debug('Changing default program directory to %s' % opt.dir)
        os.chdir(opt.dir)

    if not args[0:]:
        logging.error('You have to provide an URL address!')
        sys.exit(1)

    for arg in args:
        url = urlparse(arg)
        links = getLinks(url, opt.pageEncoding, opt.login, opt.password)

        if opt.download:
            downloadFiles(links)

        if opt.withName:
            for l in links:
                print('%s: %s' % (l[0], l[1]))
        elif not opt.download:
            for l in links:
                print(l[1])



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # Catch ^C interrupt
        logging.info('Program interrupted')
        sys.exit(1)
