#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Small path hack
import sys, os
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import urllib.parse
from datetime import datetime

import Manager

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(TESTS_DIR, 'work_files')
TEST_FILES = os.path.join(TESTS_DIR, 'test_files')

# Set working directory
os.chdir(WORK_DIR)


class ManagerTests(unittest.TestCase):

    def setUp(self):
        self._pageUrl = urllib.parse.urlparse('file://' + TEST_FILES).geturl()
        self._manager = Manager.Manager(encoding='cp1250', page=self._pageUrl)


    def test_managerInit(self):
        '''Testing manager object inicialization'''
        self.assertTrue(os.path.isdir(TEST_FILES))
        self.assertEqual(self._manager._encoding, 'cp1250')
        self.assertEqual(self._manager._page, self._pageUrl)


    def test_getIframeLinks(self):
        '''We are testing regular expression for finding iframe links'''
        url = urllib.parse.urlparse('file://' + TEST_FILES + '/Basic_Page-test-iframe-links.htm')
        iframeLinks = self._manager.getIframeLinks(url=url.geturl(), encoding='cp1250')
        
        self.assertIn(('http://titulky.com/', 'Titulky.com'), iframeLinks)
        self.assertIn(('/idown.php?R=1341223560&amp;titulky=0000000615&amp;zip=&amp;histstamp=', 'Link 1'), iframeLinks)
        self.assertIn(('http://www.titulky.com/idown.php?R=1341223560&amp;titulky=0000000615&amp;zip=&amp;histstamp=', 'Link 2'), iframeLinks)
        self.assertIn(('idown.php?R=1341223560&amp;titulky=0000000615&amp;zip=&amp;histstamp=', 'Link 3'), iframeLinks)

        # There shouldn't be other links
        self.assertIs(len(iframeLinks), 4)

                

    def test_getLinks(self):
        url = urllib.parse.urlparse('file://' + TEST_FILES + '/Some_Movie-170819.htm')
        self._manager.getSubtitleSourceLinks(url=url.geturl())

        self.assertIn({'url' : self._pageUrl + 'idown.php?id=90801970',
                       'name' : 'Some Movie (CD 1)',
                       'wait' : datetime.now().hour,
                      }, self._manager._links)

        self.assertIn({'url' : self._pageUrl + 'idown.php?id=90801970',
                       'name' : 'Some Movie (CD 2)',
                       'wait' : datetime.now().hour,
                      }, self._manager._links)

        self.assertIs(len(self._manager._links), 2)


    def test_downloadFiles(self):
        '''Test for downloading subtitle file'''
        url = urllib.parse.urlparse('file://' + TEST_FILES + '/idown.php?id=90801970')
        files = [{'name' : 'file1-downloaded', 'url' : url.geturl(), 'wait' : 0}]

        self._manager.downloadFiles(links=files)
        self.assertTrue(os.path.isfile(os.path.join(WORK_DIR) + '/file1-downloaded.srt'))

if __name__ == '__main__':
    unittest.main()
