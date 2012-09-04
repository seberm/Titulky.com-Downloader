# -*- coding: utf-8 -*-

import re
import urllib

from logging import debug, info, error, warning, exception
from datetime import datetime
from threading import Thread

from TitulkyDownloader import PAGE

titlesLinks = []

class IFrameParser(Thread):

    def __init__(self, opener, url, name, encoding, lock, page=PAGE):
        self._opener = opener
        self._url = url
        self._page = page
        self._movieName = name
        self._encoding = encoding
        self._lock = lock

        Thread.__init__(self)


    def run(self):
        global titlesLinks
        debug('[%s]: Running new IFrameParser thread (%s)' % (self._movieName, self._url))
         
        try:
            with self._opener.open(self._url) as fd:
                iframe = str(fd.read().decode(self._encoding))
        except urllib.error.URLError as e:
            error('[%s]: URL error: %s' % (self._movieName, e.reason))
        except IOError:
            error('[%s]: IO Error - thread exiting' % self._movieName)
            sys.exit(1)

        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        debug('[%s]: Parsing iframe ...' % self._movieName)

        data = re.search(pattern, iframe, re.VERBOSE)

        if data:
            debug('[%s]: Found link: %s' % (self._movieName, self._page + data.group('addr')))
            self._lock.acquire()
            titlesLinks.append({'name' : self._movieName, 'url' : self._page + data.group('addr'), 'wait' : datetime.now().hour})
            self._lock.release()
        else:
            debug('[%s]: No links found' % self._movieName)
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                warning('[%s]: You exhausted your free daily limit of downloads - it\'s necessary to re-type captcha code' % self._movieName)
            else:
                info('[%s]: Cannot find data on page' % self._movieName)

