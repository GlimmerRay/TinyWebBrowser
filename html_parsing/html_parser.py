import sys
from collections import deque
from string import ascii_letters, digits, whitespace
from itertools import zip_longest

class WhitespaceError(Exception):
    pass

class UnclosedTagError(Exception):
    pass

class PreconditionError(Exception):
    pass

class PostconditionError(Exception):
    pass

class UnmatchingTagError(Exception):
    pass

class InvalidTagCharacterError(Exception):
    pass

class InvalidKeyCharacterError(Exception):
    pass

class InvalidValueCharacterError(Exception):
    pass

class InvalidValueError(Exception):
    pass

class MissingClosingQuoteError(Exception):
    pass

class InvalidTagNameError(Exception):
    pass

class MissingClosingTagError(Exception):
    pass

class InvalidAttributeFormatError(Exception):
    pass


VALID_KEY_CHARS = set(ascii_letters + digits)
VALID_VALUE_CHARS = set(ascii_letters + digits + '-')
VALID_TAG_CHARS = set(ascii_letters)
VALID_TEXT_CHARS = set(ascii_letters + digits + whitespace) - set('<>')

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

    def shallow_eq(self, other):
        if not isinstance(other, ElementNode): # ElementNode != TextNode
            return False
        elif self.name != other.name: # <p> != <div>
            return False
        elif self.attributes != other.attributes: # <p class=x> != <p class=y>
            return False
        else:
            return True
    
    def breadthFirstIterator(self):
        queue = deque([self])
        while len(queue) > 0:
            node = queue.popleft()
            yield node
            if isinstance(node, ElementNode):
                queue.extend(node.children)

    def __eq__(self, other): # breadth-first tree traversal
        if not isinstance(other, self.__class__):
            return False
        self_tree, other_tree = self.breadthFirstIterator(), other.breadthFirstIterator()
        for self_node, other_node in zip_longest(self_tree, other_tree):
            if self_node == None or other_node == None: # the lengths are not the same
                return False
            elif not self_node.shallow_eq(other_node):
                return False
        return True
    
    def __repr__(self):
        return self.name

class TextNode:
    def __init__(self, text):
        self.text = text

    def shallow_eq(self, other):
        return self == other
    
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

class PreconditionError(Exception):

    def __init__(self, function_name, precondition):
        self.message = f'The precondition of {function_name}() is that {precondition}'
        super.__init__(self.message)

class PostconditionError(Exception):

    def __init__(self, function_name, postcondition):
        self.message = f'The postcondition of {function_name}() is that {postcondition}'
        super.__init__(self.message)


class ConsumeTagPrecondtionError(PreconditionError):

    def __init__(self):
        self.function_name = 'consume_tag'
        self.precondition = 'the cursor must be pointed at a "<"'
        super.__init__(self.function_name, self.precondition)

class ConsumeTagPostconditionError(PostconditionError):

    pass




class HtmlParser:

    def __init__(self, html):
        self.html = html # is a string
        self.cursor = 0
        self.stack = []
        self.DOM = None
        self.finished_parsing = False
    
    def parse(self):
        self.skip_whitespace() # Rule 1
        while not self.finished_parsing:
            self.consume_tag()
            self.consume_text()
        return self.DOM
    
    def skip_whitespace(self):
        while consume_char().isspace():
            continue
    
    def consume_tag(self):
        if self.peek() != '<': # Rule 2
            raise ConsumeTagPreconditionError()
        elif self.peek_at_char(forward=1) == '/':
            self.consume_closing_tag()
        else:
            self.consume_opening_tag()
        if self.peek() != '>':
            raise ConsumeTagPostconditionError()
    
    def consume_opening_tag(self):
        if self.peek() != '<':
            raise ConsumeOpeningTagPreconditionError()
        tag_name = self.get_opening_tag_name()
        element = ElementNode(tag_name)
        if self.peek() != '>':
            attrs = self.get_attributes
            element.attributes = attrs
        if self.peek() != '>':
            raise ConsumeOpeningTagPostconditionError()
        stack.append(element)

    def get_attributes(self):
        if self.peek() != ' ':
            raise GetAttributesPreconditionError()
        attrs = {}
        while self.peek() != '>':
            key, value = self.get_attribute()
            attrs[key] = value
        if self.peek() != '>':
            raise GetAttributesPostconditionError()
        return attrs
    
    def get_attribute(self):
        if self.peek() != ' ':
            raise GetAttributePreconditionError()
        self.skip(forward=1)
        key = self.consume_until('=', VALID_KEY_CHARS)
        self.skip(forward=1)
        if self.peek() == '"':
            value = self.get_quoted_value()
        else:
            value = self.consume_until({' ', '>'}, VALID_VALUE_CHARS)
        if self.peek() != ' ' and self.peek() != '>':
            raise GetAttributesPostconditionError()
        return key, value
    
    def get_quoted_value(self):
        if self.peek() != '"':
            raise GetQuotedValuePreconditionError()
        self.skip(forward=1)
        value = consume_until('"', VALID_VALUE_CHARS)
        self.skip(forward=1)
        if self.peek() != ' ' and self.peek() != '>':
            raise InvalidAttributeFormatError()
        return value
    
    def get_opening_tag_name(self):
        if self.peek() != '<':
            raise GetOpeningTagNamePreconditionError()
        self.skip(forward=1)
        tag_name = self.consume_until({' ', '>'}, VALID_TAG_NAME_CHARS)
        if tag_name == '': # Errors 1
            raise InvalidTagNameError('Tag name cannot be the empty string')
        if self.peek() != '>' and self.peek() != ' ':
            raise GetOpeningTagNamePostconditionError()
        return tag_name
    
    def consume_closing_tag(self):
        if self.peek() != '<':
            raise ConsumeClosingTagPreconditionError()
        tag_name = self.get_closing_tag_name()
        if tag_name != stack[-1].name:
            raise UnmatchingTagError()
        element = self.stack.pop()
        if len(stack) == 0:
            self.DOM = element
            self.finished_parsing = True
        else:
            stack[-1].addChild(element)
        if self.peek() != '>':
            raise ConsumeClosingTagPostconditionError()
    
    def get_closing_tag_name(self):
        if self.peek() != '<' or self.peek(forward=1) != '/':
            raise GetClosingTagNamePreconditionError()
        self.skip(forward=2)
        tag_name = consume_until('>', VALID_TAG_NAME_CHARS)
        if tag_name == '': # Errors 2
            raise InvalidTagNameError('Tag name cannot be the empty string')
        if self.peek() != '>':
            raise GetClosingTagPostconditionError()
        return tag_name

    def consume_until(stop_charset, valid_charset):
        string = []
        while self.peek() not in stop_charset:   
            char = self.consume_char()
            if char not in valid_charset:
                raise valid_charset.error
            string.append(char)
        return ''.join(string)

    def consume_text(self):
        if self.peek() != '>':
            raise ConsumeTextPreconditionError()
        text = self.get_text()
        if text != '':
            text_node = TextNode(text)
            stack[-1].addChild(text_node)
        if self.peek() != '<':
            raise ConsumeTextPostconditionError()
    
    def get_text(self):
        if self.peek() != '>':
            raise GetTextPreconditionError()
        self.skip(forward=1)
        text = self.consume_until('>', VALID_TEXT_CHARS)
        text = text.strip()
        if self.peek() != '<':
            raise GetTestPostconditionError()
        return text

    def consume_char(self):
        if self.cursor >= len(self):
            raise IndexError()
        char = self.html[self.cursor]
        self.cursor += 1
        return char

    def peek_at_char(self, forward=0):
        if self.cursor + self.foward >= len(self):
            raise IndexError()
        return self.html[self.cursor+forward]
    
    def skip(forward):
        self.cursor += forward
    
    def __length__(self):
        return len(self.html)




