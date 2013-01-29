# -*- coding: utf-8 -*-

import urllib
import logging
import threading
import re
import sys
import os
import time

from urllib import request
from urllib.parse import urlencode
from threading import Lock
from http.cookiejar import CookieJar
from logging import debug, info, error, warning, exception

import IFrameParser
from TitulkyDownloader import PAGE

# Constants
CHECK_TIME = 0.05 # secs
LOGIN_PAGE = 'http://www.titulky.com/index.php'
DOWN_WAIT_TIME = 10 # secs


class Manager(object):

    # Constants
    DEFAULTS = {
            'Encoding' : 'utf-8',
    }


    def __init__(self, encoding=''):
        self._encoding = self.DEFAULTS['Encoding']
        self._vip = False
        self._withInfo = False
        self._links = []
        self._parsers = []

        if encoding:
            self._encoding = encoding

        self._opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))


    def useVIP(self):
        self._vip = True


    def showWithInfo(self):
        self._withInfo = True


    def logIn(self, login='', password=''):
        '''
        Makes o http POST request to login script (LOGIN_PAGE)
        and internally remembers a login cookie in self._opener object
        '''

        if login and password:
            loginData = urlencode({'Login' : login, 'Password' : password, 'foreverlog' : 1})
            try:
                debug('Posting login credentials [user: %s, passowrd: %s]' % (login, len(password) * '*'))
                with self._opener.open(LOGIN_PAGE, loginData.encode(self._encoding)):
                    pass
            except urllib.error.URLError as e:
                error('URL error: %s' % e.reason)
                error('Login failed')
                sys.exit(1)


    def getIframeLinks(self, url=''):
        htmlSource = ''
        try:
            debug('Opening subtitles page: %s' % url)
            with self._opener.open(url) as fd:
                htmlSource = str(fd.read())
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
        except LookupError as e:
            error('Lookup Error: %s' % e.args)
            sys.exit(1)

        pattern = r'''
                <td                                         # TD before hyperlink (it's because program downloaded all
                                                            # titles including titles from history box
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

        debug('Looking for iframe links ...')
        return re.findall(pattern, htmlSource, re.VERBOSE)


    def getSubtitleSourceLinks(self, url):
        links = self.getIframeLinks(url.geturl())

        if links:
            lock = Lock()

            debug('Links found: %d' % len(links))
            for link in links:
                iframeURL = PAGE + '/' + link[0]
                name = link[1]
                try:
                    debug('Creating parser for iframe [%s]: %s' % (name, iframeURL))
                    parser = IFrameParser.IFrameParser(self._opener, iframeURL, name, lock, PAGE)
                    # Start thread
                    debug('[%s] Starting parser ...' % name)
                    parser.start()
                    #parser.join()
                    self._parsers.append(parser)
                except RuntimeError as e:
                    exception('Thread caused runtime error: %s' % e)
                    sys.exit(1)

            # We're active waiting for end of all threads
            # @todo Some better solution or workaround?
            # @todo Completely rewrite this
            while threading.active_count() != 1:
                time.sleep(CHECK_TIME)

            self._links = IFrameParser.titlesLinks
            debug('Subtitles links found: %d' % len(self._links))
            return self._links
        else:
            info('Cannot find data on page')
            sys.exit(1)


    def downloadFiles(self, links=[{}]):
        if not links[0]:
            links = self._links

        debug('Downloading links: %d' % len(links))

        for l in links:
            if not self._vip:
                # +2 because we should make sure that we can download
                waitTime = DOWN_WAIT_TIME + 2
                debug('[%s]: [%d secs] - %s' % (l['name'], waitTime, l['url']))

                # Waiting for download
                debug('[%s]: Waiting for download ...' % l['name'])
                time.sleep(float(waitTime))

            try:
                debug('[%s]: Downloading from: %s' % (l['name'], l['url']))
                with self._opener.open(l['url']) as fd:
                    debug('[%s]: Saving into: %s' % (l['name'], os.getcwd()))
                    with open(l['name'] + '.srt', mode='wb') as titles:
                        titles.write(fd.read())
            except urllib.error.URLError as e:
                error('[%s]: Cannot get subtitles: %s' % (l['name'], e.reason))
                sys.exit(1)
            except IOError:
                error('[%s]: Cannot open file: %s.srt' % (l['name'], l['name']))
                sys.exit(1)


    def printLinks(self, links=[]):
        if not links:
            links = self._links

        if self._withInfo:
            for l in links:
                print('[%s][after %d secs]: %s' % (l['name'], l['wait'], l['url']))
        else:
            for l in links:
                print(l['url'])


    def clean(self):
        '''
        Resets manager object
        If we call getSubtitleSourceLinks we must clean source links!
        '''
        self._links = []
