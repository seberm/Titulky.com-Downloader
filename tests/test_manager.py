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

        self.pageUrl = urllib.parse.urlparse('file://' + TEST_FILES).geturl()
        self.manager = Manager.Manager(encoding='cp1250', page=self.pageUrl)


    def test_managerInit(self):
        self.assertTrue(os.path.isdir(TEST_FILES))
        self.assertEqual(self.manager.encoding, 'cp1250')
        self.assertEqual(self.manager.page, self.pageUrl)


    def test_getLinks(self):
        url = urllib.parse.urlparse('file://' + TEST_FILES + '/Some_Movie-170819.htm')
        self.manager.getLinks(url=url.geturl())

        self.assertIn({'url' : self.pageUrl + 'idown.php?id=90801970',
                       'name' : 'Some Movie (CD 1)',
                       'wait' : datetime.now().hour,
                      }, self.manager.links)

        self.assertIn({'url' : self.pageUrl + 'idown.php?id=90801970',
                       'name' : 'Some Movie (CD 2)',
                       'wait' : datetime.now().hour,
                      }, self.manager.links)

        self.assertIs(len(self.manager.links), 2)


    def test_downloadFiles(self):
        url = urllib.parse.urlparse('file://' + TEST_FILES + '/idown.php?id=90801970')
        files = [{'name' : 'file1-downloaded', 'url' : url.geturl(), 'wait' : 0}]

        self.manager.downloadFiles(links=files)
        self.assertTrue(os.path.isfile(os.path.join(WORK_DIR) + '/file1-downloaded.srt'))

if __name__ == '__main__':
    unittest.main()
