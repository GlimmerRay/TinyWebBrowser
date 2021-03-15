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
    
    def test_tag_formatting(self):
        # < title class=thetitle>Document</title>
        test2_html = load_file('test2.html')
        with self.assertRaises(WhitespaceError):
            parse(test2_html)
        test3_html = load_file('test3.html')
        #  <title >Document</title>
        with self.assertRaises(WhitespaceError):
            parse(test3_html)
        # <title class=thetitle >Document</title>
        test4_html = load_file('test4.html')
        with self.assertRaises(WhitespaceError):
            parse(test4_html)
        # <title class =thetitle>Document</title>
        test5_html = load_file('test5.html')
        with self.assertRaises(WhitespaceError):
            parse(test5_html)
        # <title class= thetitle>Document</title>
        test6_html = load_file('test6.html')
        with self.assertRaises(Exception):
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
        # <div class=></div>
        test10_html = load_file('test10.html')
        with self.assertRaises(Exception):
            parse(test10_html)
        # <div class= ></div>
        test11_html = load_file('test11.html')
        with self.assertRaises(Exception):
            parse(test11_html)
        # <div class></div>
        test12_html = load_file('test12.html')
        with self.assertRaises(Exception):
            parse(test12_html)
    
    def test_whitespace_in_text(self):
        test13_html = load_file('test13.html')
        test14_html = load_file('test14.html')
        test13_dom = parse(test13_html)
        test14_dom = parse(test14_html)
        # <div></div> == <div>        </div>
        self.assertEqual(test13_dom, test14_dom)

        test15_html = load_file('test15.html')
        test16_html = load_file('test16.html')
        test17_html = load_file('test17.html')
        test18_html = load_file('test18.html')
        test19_html = load_file('test19.html')
        test20_html = load_file('test20.html')
        test21_html = load_file('test21.html')
        test22_html = load_file('test22.html')
        test23_html = load_file('test23.html')

        test15_dom = parse(test15_html)
        test16_dom = parse(test16_html)
        test17_dom = parse(test17_html)
        test18_dom = parse(test18_html)
        test19_dom = parse(test19_html)
        test20_dom = parse(test20_html)
        test21_dom = parse(test21_html)
        test22_dom = parse(test22_html)
        
        # With spaces:
        # <div>   abc</div> == <div>abc</div>
        self.assertEqual(test16_dom, test15_dom)
        # <div>abc   </div> == <div>abc</div>
        self.assertEqual(test17_dom, test15_dom)
        # <div>   abc   </div> == <div>abc</div>
        self.assertEqual(test18_dom, test15_dom)

        # With tabs:
        # <div>     abc</div> == <div>abc</div>
        self.assertEqual(test19_dom, test15_dom)
        # <div>abc      </div> == <div>abc</div>
        self.assertEqual(test20_dom, test15_dom)
        # <div>     abc     </div> == <div>abc</div>
        self.assertEqual(test21_dom, test15_dom)


        # <div>abc</div> == 
        # <div>
        #       abc
        # </div>
        self.assertEqual(test22_dom, test15_dom)

    def test_quoted_values(self):
        test1_html = load_file('test1.html')
        test1_dom = parse(test1_html)
        test23_html = load_file('test23.html')
        test23_dom = parse(test23_html)
        # <title class=thetitle>Document</title> equals
        # <title class="thetitle">Document</title>
        self.assertEqual(test1_dom, test23_dom)

        # <title class="thetitle>Document</title>
        test24_html = load_file('test24.html')
        with self.assertRaises(Exception):
            parse(test24_html)
    
    # def test_valid_characters(self):
        

if __name__ == '__main__':
    unittest.main()
    # html = load_file('test1.html')
    # dom = parse(html)
    # tree = dom.breadthFirstIterator()
    # for node in tree:
    #     print(node)