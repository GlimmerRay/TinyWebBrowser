import sys
sys.path.insert(0, '/Users/brandonhodges/Desktop/tiny_web_browser/')

import os
from html_parsing.html_parser import *
import unittest
from html_parsing.testing.dom_tests import *

TEST_DIR = 'html_parsing/testing/html_test_files/'

# takes a file name, loads it from TEST_DIR, and returns its contents as a string
def load_file(filename):
    path = os.path.join(TEST_DIR, filename)
    with open(path, 'r') as f:
        contents = ''.join(f.readlines())
    return contents

class TestStringMethods(unittest.TestCase):

    def test_parse1(self):
        test1_html = load_file('test1.html')
        dom = parse(test1_html)
        self.assertEquals(dom, dom1())
    
    


if __name__ == '__main__':
    unittest.main()