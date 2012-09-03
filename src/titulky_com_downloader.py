#!/usr/bin/env python3
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

import re
import sys
import os
import threading
import logging

from getpass import getpass
#from urllib import request
#from urllib.parse import urlparse, urlencode
from http import cookiejar

# @deprecated
from optparse import OptionParser, OptionGroup

# Globals
NAME = 'titulky_com_downloader'
VERSION = '1.0.0'

PAGE = 'http://www.titulky.com'

DEFAULT_LOGGING_LEVEL = 'INFO' #logging.INFO
DEFAULT_LOGGING_FORMAT = '%(levelname)s: %(message)s'

PAGE_ENCODING = 'cp1250'
CHECK_TIME = 0.05 #s


def main():
    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [OPTION]... [URL]...',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)',
                          version = '%prog ' + VERSION)

    options = OptionGroup(parser, 'Program Options', 'Options specific to titulky_com_downloader.')
    
    options.add_option('-l', '--link', dest='link', action='store_true', help='Print download link(s) on stdout (default behaviour)')
    options.add_option('-e', '--page-encoding', dest='pageEncoding', action='store', metavar='<encoding>', default=PAGE_ENCODING, help='Sets webpage encoding - default [cp1250]')
    options.add_option('-n', '--with-info', dest='withInfo', action='store_true', help='Print download links with movie name and number of secs to link activation')
    options.add_option('-p', '--dir', dest='dir', action='store', help='Change program directory')
    options.add_option('--login', dest='login', action='store_true', help='Login to netusers.cz (titulky.com)')
    options.add_option('--log', dest='logLevel', action='store', default=DEFAULT_LOGGING_LEVEL, help='Set logging level (debug, info, warning, error, critical)')
    options.add_option('-i', '--vip', dest='vip', action='store_true', help='Set up a VIP user download (we don\'t want to wait for download)')

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

    from Manager import Manager
    manager = Manager()

    for arg in args:
        url = urlparse(arg)

        if opt.login:
            manager.login = input('[netusers.cz] Login: ')
            manager.password = getpass('[netusers.cz] Password: ')

        links = getLinks(url.geturl(), opt.pageEncoding, login, password)

        if opt.download:
            downloadFiles(links, opt.vip)

        if opt.withInfo:
            for l in links:
                print('[%s][after %d secs]: %s' % (l['name'], l['wait'], l['url']))
        elif not opt.download:
            for l in links:
                print(l['url'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # Catch ^C interrupt
        logging.info('Program interrupted')
        sys.exit(1)
