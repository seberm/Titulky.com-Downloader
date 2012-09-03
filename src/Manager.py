import urllib
import logging
import time

from cookiejar import CookieJar
from urllib import request
from urllib.parse import urlparse, urlencode
from threading import Lock
#from logging import debug, info, error, warning, exception

import IFrameParser
from IFrameParser import IFrameParser



class Manager:

    # Constants
    DEFAULTS = {
            'Encoding' : 'cp1250',
    }


    def __init__(self, conf={}):
        self.encoding = DEFAULTS['Encoding']
        self.login = ''
        self.password = ''
        self.url = ''
        self.links = []
        self.parsers = []

        if conf['encoding']:
            self.encoding = conf['encoding']

        if conf['url']:
            self.encoding = conf['url']

        self.opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))


    def login(self, credentials={}):
        if credentials['login']:
            self.login = credentials['login']

        if credentials['password']:
            self.password = credentials['password']

        if self.login and self.password:
            loginData = urlencode({'Login' : self.login, 'Password' : self.password, 'foreverlog' : 1})
            try:
                logging.debug('Posting login credentials [user: %s]' % self.login)
                self.opener.open('http://www.titulky.com/index.php', loginData.encode(encoding))
            except urllib.error.URLError as e:
                logging.error('URL error: %s' % e.reason)
                logging.error('Login failed')
                sys.exit(1)


    def getLinks(self, url='', conf={}):
        encoding = self.encoding
        if conf['encoding']:
            encoding = conf['encoding']

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
                    parser = IFrameParser(self.opener, iframeURL, name, encoding, lock)
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
