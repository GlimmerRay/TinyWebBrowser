import sys
sys.path.insert(0, '/Users/brandonhodges/Desktop/tiny_web_browser/')

import os
from html_parsing.html_parser import *
import unittest

TEST_DIR = 'html_parsing/testing/html_test_files/'

# takes a file name
# loads it from TEST_DIR
# and returns its contents as a string
def load_file(filename):
    path = os.path.join(TEST_DIR, filename)
    with open(path, 'r') as f:
        contents = ''.join(f.readlines())
    return contents

test1 = load_file('test1.html')

class TestStringMethods(unittest.TestCase):

    def test_parse1(self):
        # html1 = "</div><div class=blue id=white>Some text</div>"
        # print(get_attributes(html1, 10))
        test1 = load_file('test1.html')
        dom = parse(test1)
        self.assertEqual(dom.name, 'html')
        self.assertEqual(len(dom.children), 2)
        self.assertEqual(dom.children[0].name, 'head')
        self.assertEqual(dom.children[1].name, 'body')
        self.assertEqual(len(dom.children[0].children), 1)
        self.assertEqual(dom.children[0].children[0].name, 'title')
        self.assertEqual(len(dom.children[0].children[0].children), 1)
        self.assertEqual(dom.children[0].children[0].children[0].text, 'Document')
        self.assertEqual(len(dom.children[1].children), 0)

if __name__ == '__main__':
    unittest.main()