#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Small path hack
import sys, os
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import urllib.parse
from datetime import datetime

import Manager

PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')

class ManagerTests(unittest.TestCase):

    def setUp(self):

        self.pageUrl = urllib.parse.urlparse('file://' + PAGE).geturl()
        self.manager = Manager.Manager(encoding='cp1250', page=self.pageUrl)


    def test_managerInit(self):
        self.assertTrue(os.path.isdir(PAGE))
        self.assertEqual(self.manager.encoding, 'cp1250')
        self.assertEqual(self.manager.page, self.pageUrl)


    def test_getLinks(self):
        url = urllib.parse.urlparse('file://' + PAGE + '/Some_Movie-170819.htm')
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

if __name__ == '__main__':
    unittest.main()
