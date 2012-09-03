# -*- coding: utf-8 -*-

# Copyright (C) 2012 Seberm (Otto Sabart)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# (version 3) as published by the Free Software Foundation.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
#from logging import debug, info, error, warning, exception

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
                logging.debug('Posting login credentials [user: %s]' % login)
                self.opener.open('http://www.titulky.com/index.php', loginData.encode(self.encoding))
            except urllib.error.URLError as e:
                logging.error('URL error: %s' % e.reason)
                logging.error('Login failed')
                sys.exit(1)


    def getLinks(self, url='', encoding=''):
        if not encoding:
            encoding = self.encoding

        htmlSource = ''
        try:
            fd = self.opener.open(url)
            htmlSource = str(fd.read().decode(encoding))
        except urllib.error.HTTPError as e:
            logging.error('HTTP Connection error (%d): %s' % (e.code, e.reason))
            sys.exit(1)
        except urllib.error.URLError as e:
            logging.error('[%s]: URL error: %s' % (url, e.reason))
            sys.exit(1)
        except IOError:
            logging.error('Cannot read page data - %s' % url)
            sys.exit(1)
        except ValueError:
            logging.error('URL value error: Unknown URL type: %s' % url)
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

        logging.debug('Looking for subtitles links on %s' % url)
        links = re.findall(pattern, htmlSource, re.VERBOSE)

        if links:
            lock = Lock()

            logging.debug('Links found: %d' % len(links))
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
                    logging.exception('Thread caused runtime error: %s' % e)
                    sys.exit(1)

            # We're active waiting for end of all threads
            # @todo Some better solution or workaround?
            # @todo Completely rewrite this
            while threading.active_count() != 1:
                time.sleep(CHECK_TIME)

            self.links = IFrameParser.titlesLinks
            return self.links
        else:
            logging.info('Cannot find data on page')
            sys.exit(1)


    def downloadFiles(self, userVIP=False):
        logging.debug('Downloading links: %d' % len(self.links))

        for l in self.links:
            if not userVIP:
                # +2 because we should make sure that we can download
                waitTime = l['wait'] + 2

                logging.debug('[%s][%d secs] - %s' % (l['name'], waitTime, l['url']))
                logging.debug('[%s]: Waiting for download ...' % l['name'])

                # Waiting for download
                time.sleep(float(waitTime))
            try:
                logging.debug('[%s]: Downloading from: %s' % (l['name'], l['url']))
                fd = request.urlopen(l['url'])

                with open(l['name'] + '.srt', mode='wb') as titles:
                    titles.write(fd.read())

                fd.close()
            except urllib.error.URLError as e:
                logging.error('[%s]: Cannot get subtitles: %s' % (l['name'], e.reason))
                sys.exit(1)
            except IOError:
                logging.error('[%s]: Cannot open file: %s.srt' % (l['name'], l['name']))
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


