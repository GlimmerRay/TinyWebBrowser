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

    def test_basic(self):
        test1_html = load_file('test1.html')
        dom = parse(test1_html)
        self.assertEqual(dom, dom1())
    
    def whitespace_in_tag(self):
        # < title class=thetitle>Document</title>
        test2_html = load_file('test2.html')
        with self.assertRaises(WhitespaceError):
            parse(test2_html)
        test3_html = load_file('test3.html')
        #  <title >Document</title>
        with self.assertRaises(WhitespaceError):
            parse(test3_html)
        # < title class=thetitle >Document</title>
        test4_html = load_file('test4.html')
        with self.assertRaises(WhitespaceError):
            parse(test4_html)
        # <title class =thetitle>Document</title>
        test5_html = load_file('test5.html')
        with self.assertRaises(WhitespaceError):
            parse(test5_html)
        # <title class= thetitle>Document</title>
        test6_html = load_file('test6.html')
        with self.assertRaises(WhitespaceError):
            parse(test6_html)
        # <title class=thetitle  id=someid>Document</title>
        # note: there are two spaces between the attributes
        test7_html = load_file('test7.html')
        with self.assertRaises(WhitespaceError):
            parse(test7_html)
        # <title class=thetitle>Document< /title>
        test8_html = load_file('test8.html')
        with self.assertRaises(WhitespaceError):
            parse(test8_html)
        # <title class=thetitle>Document</title >
        test9_html = load_file('test9.html')
        with self.assertRaises(WhitespaceError):
            parse(test9_html)
    
    # def test_whitespace_in_text(self):
    #     test10_html = load_file('test10.html')
    #     test11_html = load_file('test11.html')
    #     test10_dom = parse(test10_html)
    #     test11_dom = parse(test11_html)
    #     self.assertEquals(test10_dom, test11_dom)
        

if __name__ == '__main__':
    unittest.main()