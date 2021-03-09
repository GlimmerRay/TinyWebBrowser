import sys
sys.path.insert(0, '/Users/brandonhodges/Desktop/tiny_web_browser/')
import os
from html_parsing.html_parser import parse

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
    test1 = load_file('test1.html')
    parse(test1)

