import sys
sys.path.insert(0, '/Users/brandonhodges/Desktop/tiny_web_browser/')
import os
from html_parsing.html_parser import *

TEST_DIR = 'html_test_files/'

# takes a file name
# loads it from TEST_DIR
# and returns its contents as a string
def load_file(filename):
    path = os.path.join(TEST_DIR, filename)
    with open(path, 'r') as f:
        contents = ''.join(f.readlines())
    return contents

if __name__ == '__main__':
    assert consume_elem_name('<div>', 0) == ('div', 4)
    assert consume_elem_name('abcdefg<div>', 7) == ('div', 11)
    assert consume_elem_name('<fruit>', 0) == ('fruit', 6)
    assert consume_elem_name('abcdefg<fruit>', 7) == ('fruit', 13)
    
    test1 = load_file('test1.html')
    dom = parse(test1)
    assert dom.name == 'html'
    assert len(dom.children) == 2
    assert dom.children[0].name == 'head'
    assert dom.children[1].name == 'body'
    assert len(dom.children[0].children) == 1
    assert dom.children[0].children[0].name == 'title'
    assert len(dom.children[0].children[0].children) == 1
    assert dom.children[0].children[0].children[0].text == 'Document'
    assert len(dom.children[1].children) == 0

