import os

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
    print(load_file('test1.html'))

