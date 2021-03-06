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


# Function which checks if module exists
def module_exists(name):
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True

import re
import sys
import os
import logging

from logging import debug, info, error, warning, exception

from urllib.parse import urlparse
from getpass import getpass

# @deprecated
from optparse import OptionParser, OptionGroup

# Globals
NAME = 'titulky_com_downloader'
VERSION = '1.0.0'

PAGE = 'http://www.titulky.com'

DEFAULT_LOGGING_LEVEL = 'INFO' #logging.INFO
DEFAULT_LOGGING_FORMAT = '%(levelname)s: %(message)s'

PAGE_ENCODING = 'utf-8'


def main():
    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [OPTION]... [URL]...',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)',
                          version = '%prog ' + VERSION)

    options = OptionGroup(parser, 'Program Options', 'Options specific to titulky_com_downloader.')
    
    options.add_option('-l', '--link', dest='link', action='store_true',
            help='Print download link(s) on stdout (default behaviour)')
    options.add_option('-e', '--page-encoding', dest='pageEncoding', action='store', metavar='<encoding>', default=PAGE_ENCODING,
            help='Sets webpage encoding - default [cp1250]')
    options.add_option('-n', '--with-info', dest='withInfo', action='store_true',
            help='Print download links with movie name and number of secs to link activation')
    options.add_option('-p', '--dir', dest='dir', action='store',
            help='Change program directory')
    options.add_option('--login', dest='login', action='store_true',
            help='Login to netusers.cz (titulky.com)')
    options.add_option('--log', dest='logLevel', action='store', default=DEFAULT_LOGGING_LEVEL,
            help='Set logging level (debug, info, warning, error, critical)')
    options.add_option('-i', '--vip', dest='vip', action='store_true',
            help='Set up a VIP user download (we don\'t want to wait for download)')

    # @todo Remove warning message in following option
    options.add_option('-d', '--download', dest='download', action='store_true',
            help='Download subtitles to current folder (sometimes does not work - use option -l in combination with wget - just take a look to README)')

    # @todo it will be possible to add prefix to downloaded files
    #options.add_option('--prefix', dest='prefix', action='store_true',
    #       help='Set prefix to downloaded files')

    # @todo will be possible to download with direct link
    #options.add_option('--direct-link', dest='directLink', action='store_true',
    #       help='Direct link to iframe')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()

    # Do some logging stuff
    try:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=opt.logLevel.upper())
        debug('Setting logging mode to: %s' % opt.logLevel.upper())
    except ValueError:
        logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=DEFAULT_LOGGING_LEVEL)
        warning('It is not possible to set logging level to %s' % opt.logLevel.upper())
        warning('Using default setting logging level: %s' % DEFAULT_LOGGING_LEVEL)

    if opt.dir:
        debug('Changing default program directory to %s' % opt.dir)
        os.chdir(opt.dir)

    if not args[0:]:
        error('You have to provide an URL address!')
        sys.exit(1)

    debug('Page encoding: %s' % opt.pageEncoding)
    from Manager import Manager
    manager = Manager(encoding=opt.pageEncoding)

    if opt.login:
        login = input('[netusers.cz] Login: ')
        password = getpass('[netusers.cz] Password: ')
        manager.logIn(login=login, password=password)

    if opt.vip:
        manager.userVIP()

    for arg in args:
        manager.getSubtitleSourceLinks(urlparse(arg))

        if opt.download:
            manager.downloadFiles()

        if opt.withInfo:
            manager.showWithInfo()

        if opt.withInfo or not opt.download:
            manager.printLinks()

        manager.clean()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # Catch ^C interrupt
        info('Program interrupted')
        sys.exit(1)
