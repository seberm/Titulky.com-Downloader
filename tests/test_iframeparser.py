#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Small path hack
import sys, os
sys.path.insert(0, os.path.abspath('../src'))

import unittest
from threading import Lock

import IFrameParser

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(TESTS_DIR, 'work_files')
TEST_FILES = os.path.join(TESTS_DIR, 'test_files')

# Set working directory
os.chdir(WORK_DIR)


class IFrameParserTests(unittest.TestCase):

    def setUp(self):
        pass


    def test_getSourceLink(self):
        content = ''
        with open(os.path.join(TEST_FILES, 'iframe-normal-unlogged.php'), 'r', encoding='cp1250') as fd:
            content = fd.read()
        
        link = IFrameParser.IFrameParser.getSourceLink(content)
        self.assertTrue(link)
        self.assertEqual(link.group('addr'), 'idown.php?id=90801970')



if __name__ == '__main__':
    unittest.main()
