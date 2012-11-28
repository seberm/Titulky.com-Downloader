# -*- coding: utf-8 -*-

import re
import urllib

from logging import debug, info, error, warning, exception
from datetime import datetime
from threading import Thread, Lock

from TitulkyDownloader import PAGE, PAGE_ENCODING, module_exists

titlesLinks = []

from PyQt4.QtCore import QThread
from PyQt4 import QtCore


class IFrameParser(QThread):

    def __init__(self, opener=None, url='', name='', encoding=PAGE_ENCODING, lock = Lock(), page=PAGE, code=''):
        if not opener:
            opener = urllib.request

        self._opener = opener
        self._url = url
        self._page = page
        self._movieName = name
        self._encoding = encoding
        self._lock = lock
        self._code = code

        QThread.__init__(self)

    
    def getSourceLink(content=''):
        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        return re.search(pattern, content, re.VERBOSE)


    def run(self):
        global titlesLinks
        debug('[%s]: Running new IFrameParser thread (%s)' % (self._movieName, self._url))

        data = None
        if self._code:
            debug('[%s]: Got captcha code (%s), trying to POST code ...' % (self._movieName, self._code))
            from urllib.parse import urlencode
            data = urlencode({'downkod' : self._code, 'titulky': 204927, 'histstamp' : 1352377345})
            debug('[%s]: POST request is: %s' % (self._movieName, data))
         
        try:
            with self._opener.open(self._url, data) as fd:
                iframe = str(fd.read().decode(self._encoding))
        except urllib.error.URLError as e:
            error('[%s]: URL error: %s' % (self._movieName, e.reason))
        except IOError:
            error('[%s]: IO Error - thread exiting' % self._movieName)
            sys.exit(1)

        debug('[%s]: Getting source link from iframe ...' % self._movieName)
        sourceLink = IFrameParser.getSourceLink(iframe) 
        if sourceLink:
            debug('[%s]: Found link: %s' % (self._movieName, self._page + sourceLink.group('addr')))
            self._lock.acquire()
            titlesLinks.append({'name' : self._movieName, 'url' : self._page + sourceLink.group('addr'), 'wait' : datetime.now().hour})
            self._lock.release()
        else:
            debug('[%s]: No links found' % self._movieName)
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                warning('[%s]: You exhausted your free daily limit of downloads - it\'s necessary to re-type captcha code' % self._movieName)
                debug('[%s]: Trying to read captcha code ...' % self._movieName)
                self.emit(QtCore.SIGNAL('readCode'), self._url, self._movieName)
                return
            else:
                info('[%s]: Cannot find source link on page' % self._movieName)

