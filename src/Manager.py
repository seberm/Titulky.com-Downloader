# -*- coding: utf-8 -*-

import urllib
import logging
import threading
import re
import sys
import time

from urllib import request
from urllib.parse import urlencode
from threading import Lock
from http.cookiejar import CookieJar
from logging import debug, info, error, warning, exception

import IFrameParser
from TitulkyDownloader import PAGE

# Constants
CHECK_TIME = 0.05 #s


class Manager:

    # Constants
    DEFAULTS = {
            'Encoding' : 'cp1250',
    }


    def __init__(self, encoding='', url=''):
        self.encoding = self.DEFAULTS['Encoding']
        self.login = ''
        self.password = ''
        self.url = ''
        self.links = []
        self.parsers = []

        if encoding:
            self.encoding = encoding

        if url:
            self.encoding = url

        self.opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))


    def logIn(self, login='', password=''):
        if not login:
            login = self.login

        if not password:
            password = self.password

        if login and password:
            loginData = urlencode({'Login' : login, 'Password' : password, 'foreverlog' : 1})
            try:
                debug('Posting login credentials [user: %s]' % login)
                self.opener.open('http://www.titulky.com/index.php', loginData.encode(self.encoding))
            except urllib.error.URLError as e:
                error('URL error: %s' % e.reason)
                error('Login failed')
                sys.exit(1)


    def getLinks(self, url='', encoding=''):
        if not encoding:
            encoding = self.encoding

        htmlSource = ''
        try:
            fd = self.opener.open(url)
            htmlSource = str(fd.read().decode(encoding))
        except urllib.error.HTTPError as e:
            error('HTTP Connection error (%d): %s' % (e.code, e.reason))
            sys.exit(1)
        except urllib.error.URLError as e:
            error('[%s]: URL error: %s' % (url, e.reason))
            sys.exit(1)
        except IOError:
            error('Cannot read page data - %s' % url)
            sys.exit(1)
        except ValueError:
            error('URL value error: Unknown URL type: %s' % url)
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

        debug('Looking for subtitles links on %s' % url)
        links = re.findall(pattern, htmlSource, re.VERBOSE)

        if links:
            lock = Lock()

            debug('Links found: %d' % len(links))
            for link in links:
                iframeURL = PAGE + '/' + link[0]
                name = link[1]
                try:
                    parser = IFrameParser.IFrameParser(self.opener, iframeURL, name, encoding, lock)
                    # Start thread
                    parser.start()
                    #parser.join()
                    self.parsers = parser
                except RuntimeError as e:
                    exception('Thread caused runtime error: %s' % e)
                    sys.exit(1)

            # We're active waiting for end of all threads
            # @todo Some better solution or workaround?
            # @todo Completely rewrite this
            while threading.active_count() != 1:
                time.sleep(CHECK_TIME)

            self.links = IFrameParser.titlesLinks
            return self.links
        else:
            info('Cannot find data on page')
            sys.exit(1)


    def downloadFiles(self, userVIP=False):
        debug('Downloading links: %d' % len(self.links))

        for l in self.links:
            if not userVIP:
                # +2 because we should make sure that we can download
                waitTime = l['wait'] + 2

                debug('[%s][%d secs] - %s' % (l['name'], waitTime, l['url']))
                debug('[%s]: Waiting for download ...' % l['name'])

                # Waiting for download
                time.sleep(float(waitTime))
            try:
                debug('[%s]: Downloading from: %s' % (l['name'], l['url']))
                fd = request.urlopen(l['url'])

                with open(l['name'] + '.srt', mode='wb') as titles:
                    titles.write(fd.read())

                fd.close()
            except urllib.error.URLError as e:
                error('[%s]: Cannot get subtitles: %s' % (l['name'], e.reason))
                sys.exit(1)
            except IOError:
                error('[%s]: Cannot open file: %s.srt' % (l['name'], l['name']))
                sys.exit(1)


    def printLinks(self, withInfo=False, links=[]):
        if not links:
            links = self.links

        if withInfo:
            for l in links:
                print('[%s][after %d secs]: %s' % (l['name'], l['wait'], l['url']))
        else:
            for l in links:
                print(l['url'])


