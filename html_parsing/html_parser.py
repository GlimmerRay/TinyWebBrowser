import sys

# name must be a string
# attributes musst be a dictionary of strings mapping to strings
# children must be a list of Nodes
class ElementNode:

    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.children = []
    
    def addChild(self, child):
        self.children.append(child)
    
    def __repr__(self):
        return self.name

class TextNode:
    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return self.text

# consume tag
# consume text
# consume tag
# consume text
# ...

# consume tag
    # if opening tag
        # stack it
    # else if closing tag
        # if matches top of stack
            # elem = pop top of stack
            # if stack is not empty
                #  add elem to children of the previous element
            # else
                # return the elem
        # else
            # error
    # move i past the end of the tag

# consume text
    # get the text
    # if it's empty, do nothing
    # else add it to children of top of stack

def parse(html):
    stack = []
    i = 0
    while html[i].isspace(): # white space at the top of an html document is ignored
        i += 1
    while True:
        elem, i = consume_tag(html, i, stack)
        if elem != None: # TODO: this seems odd
            return elem
        i = consume_text(html, i, stack)

def consume_tag(html, i, stack):
    if html[i] != '<': # consume_tag() assumes that i points to an open angled bracket
        raise Exception('html[i] must refer to an open angled bracket')
    if html[i+1] == '/': # indicates a closing tag
        return consume_closing_tag(html, i, stack)
    return consume_opening_tag(html, i, stack)

def consume_opening_tag(html, i, stack):
    if html[i] != '<':
        raise Exception('html[i] must refer to an open angled bracket')
    name, i = get_tag_name(html, i, open=True)
    elem = ElementNode(name)
    if html[i] == ' ':
        attrs, i = get_attributes(html, i)
        elem.attributes = attrs
    stack.append(elem)
    return None, i

def consume_closing_tag(html, i, stack):
    if html[i] != '<':
        raise Exception('html[i] must refer to an open angled bracket')
    name, i = get_tag_name(html, i, open=False)
    if name != stack[-1].name: # uh oh
        raise Exception('tag pair does not match')
    else: # we found a valid closing tag
        elem = stack.pop()
        if len(stack) == 0: # finished processing
            return elem, i
        else:
            stack[-1].addChild(elem)
            return None, i

# after this function runs, i should be pointed at either a ' ' or a '>'
def get_tag_name(html, i, open):
    if html[i] != '<':
        raise Exception('html[i] must refer to an open angled bracket')
    left, right = i+1, i+1
    if not open:
        left, right = left+1, right+1 # skip the slash
    while html[right] != '>' and html[right] != ' ':
        right += 1
        if right >= len(html):
            raise Exception('tag was never closed')
    elem_name = html[left:right]
    if elem_name == '':
        raise Exception('element name can\'t be the empty string')
    return elem_name, right

def consume_text(html, i, stack):
    text, i = get_text(html, i)
    if text != None:
        text_node = TextNode(text)
        stack[-1].addChild(text_node)
    return i

def get_text(html, i):
    if html[i] != '>':
        raise Exception('html[i] must refer to a closed angled bracket')
    left = i+1
    right = i+1 
    while html[right] != '<':
        right += 1
        if right >= len(html):
            raise Exception('text is not enclosed by a tag')
    text = html[left:right]
    text = text.strip()
    if text == '':
        return None, right
    return text, right

def get_attributes(html, i):
    if html[i] != ' ':
        raise Exception('get_attributes() expects i to be pointed at a space')
    attrs = {}
    while html[i] != '>':
        key, value, i = get_attribute(html, i)
        attrs[key] = value
    return attrs, i

def get_attribute(html, i):
    if html[i] != ' ':
        raise Exception('get_attributes() expects i to be pointed at a space')
    # i = skip_whitespace(html, i)
    while html[i].isspace():
        i += 1
    j = i
    while html[j] != '=':
        j += 1
    key = html[i:j]
    j += 1
    i = j
    while html[j] != ' ' and html[j] != '>':
        j += 1
    value = html[i:j]
    return key, value, j
