import sys
from collections import deque


class WhitespaceError(Exception):
    pass

class UnclosedTagError(Exception):
    pass

class PreconditionError(Exception):
    pass

class UnmatchingTagError(Exception):
    pass

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
    
    def __eq__(self, other): # breadth-first tree traversal
        self_queue = deque([self])
        other_queue = deque([other])
        while len(self_queue) > 0:
            self_node = self_queue.popleft()
            other_node = other_queue.popleft()
            if isinstance(self_node, ElementNode) and isinstance(other_node, ElementNode):
                if not (self_node.name == other_node.name and \
                self_node.attributes == other_node.attributes and \
                len(self_node.children) == len(other_node.children)):
                    return False
                for i in range(len(self_node.children)):
                    self_queue.append(self_node.children[i])
                    other_queue.append(other_node.children[i])
            elif isinstance(self_node, TextNode) and isinstance(other_node, TextNode):
                if not (self_node == other_node):
                    return False
            else: # Wrong types or unmatching types
                return False
        return True
    
    def __repr__(self):
        return self.name

class TextNode:
    def __init__(self, text):
        self.text = text
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        if not (self.text == other.text):
            return False
        return True
    
    def __repr__(self):
        return self.text
#parse
    # consume tag
    # consume text
    # consume tag
    # consume text
    # consume tag
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
                # return the elem (parsing is complete)
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
    if html[i+1].isspace():
        raise WhitespaceError()
    if html[i+1] == '/': # indicates a closing tag
        tag_name, i = consume_closing_tag(html, i, stack)
        if html[i] == ' ':
            raise WhitespaceError()
        return tag_name, i   
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
    name, i = get_closing_tag_name(html, i, open=False)
    if name != stack[-1].name: # uh oh
        raise UnmatchingTagError('tag pair does not match')
    else: # we found a valid closing tag
        elem = stack.pop()
        if len(stack) == 0: # finished processing
            return elem, i
        else:
            stack[-1].addChild(elem)
            return None, i

# a closing tag name is defined as a sequence of valid tag name characters
# preced by a '<\' and followed by a '>'
def get_closing_tag_name(html, i, open):
    if html[i] != '<':
        raise PreconditionError('get_closing_tag_name() requires that i \
                                 be pointed at a \'>\' character')
    if html[i+1] != '/':
        raise PreconditionError('get_closing_tag_name() requires that i+1 \
                                 be pointed at a \'/\' characer')
    left, right = i+2, i+2
    while html[right] != '>':
        # TODO: incorporate ALL invalid characters into this code
        if html[right].isspace():
            # catches: </ div> </div > </d iv> </ >
            raise WhitespaceError('No spaces allowed in closing tag.')
        right += 1
        if right >= len(html):
            raise UnclosedTagError('Reached end of file before tag was closed.')
    tag_name = html[left:right]
    if tag_name == '':
        # catches: </>
        raise InvalidTagNameError('Tag name cannot be the empty string')
    return tag_name, i
    

# an opening tag name is defined as a sequence of valid tag name characters
# preceded by a '<' and followed by a ' ' or a '>'
def get_opening_tag_name(html, i, open):
    if html[i] != '<':
        raise PreconditionError('get_opening_tag_name() requires that i \
                                 be pointed at a \'>\' character')
    left, right = i+1, i+1
    # either reach the end of the tag or the beginning of the attributes
    while html[right] != '>' and html[right] != ' ':
        right += 1
        if right >= len(html):
            raise UnclosedTagError('Reached end of file before tag was closed.')
    tag_name = html[left:right]
    if tag_name == '':
        # catches: <> < > < class=someclass>
        raise InvalidTagNameError('Tag name cannot be the empty string')
    return tag_name, i

# # after this function runs, i should be pointed at either a ' ' or a '>'
# def get_tag_name(html, i, open):
#     if html[i] != '<':
#         raise Exception('html[i] must refer to an open angled bracket')
#     left, right = i+1, i+1
#     if not open: # we're dealing w/ a closing tag
#         left, right = left+1, right+1 # skip the slash
#     while html[right] != '>' and html[right] != ' ':
#         right += 1
#         if right >= len(html):
#             raise Exception('tag was never closed')
#     elem_name = html[left:right]
#     if elem_name == '':
#         raise Exception('element name can\'t be the empty string')
#     return elem_name, right

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
    if html[i+1].isspace() or html[i+1] == '>':
        raise WhitespaceError()
    j = i
    while html[j] != '=':
        j += 1
        if html[j].isspace():
            print('x')
            raise WhitespaceError('key name can\'t have a space in it')
    key = html[i:j]
    j += 1
    i = j
    while html[j] != ' ' and html[j] != '>':
        j += 1
    value = html[i:j]
    return key, value, j
