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
        raise PreconditionError('The precondtion of consume_tag() is that i must be \
pointed at a "<"')
    if html[i+1].isspace():
        raise WhitespaceError()
    if html[i+1] == '/': # indicates a closing tag
        elem, i = consume_closing_tag(html, i, stack)  
    else:
        elem, i = consume_opening_tag(html, i, stack)
    if html[i] != '>':
        raise PostconditionError('The postcondtion of consume_tag() is that i must be pointed at a ">"')
    return elem, i

def consume_opening_tag(html, i, stack):
    name, i = get_opening_tag_name(html, i)
    elem = ElementNode(name)
    if html[i] == ' ':
        attrs, i = get_attributes(html, i)
        elem.attributes = attrs
    stack.append(elem)
    return None, i

def consume_closing_tag(html, i, stack):
    name, i = get_closing_tag_name(html, i)
    if name != stack[-1].name: # uh oh
        raise UnmatchingTagError(f'Name of closing tag does "{name}" not match \
            ')
    else: # we found a valid closing tag
        elem = stack.pop()
        if len(stack) == 0: # finished processing
            return elem, i
        else:
            stack[-1].addChild(elem)
            return None, i

# a closing tag name is defined as a sequence of valid tag name characters
# preceded by a '<\' and followed by a '>'
def get_closing_tag_name(html, i):
    if html[i] != '<':
        raise PreconditionError('The precondition of get_closing_tag_name() is that i must be \
pointed at a "<"')
    if html[i+1] != '/':
        raise PreconditionError('The precondtion of get_closing_tag_name() is that i+1 must be pointed \
at a "/"')
    left, right = i+2, i+2 # skip to (hopefully) the first char of the tag name
    while html[right] != '>':
        # TODO: incorporate ALL invalid characters into this code
        if html[right].isspace():
            # catches: </ div> </div > </d iv> </ >
            raise WhitespaceError('No spaces allowed in closing tag.')
        if html[right] not in VALID_TAG_CHARS:
            raise InvalidTagCharacterError(f'The character {html[right]} is not a valid tag character.')
        right += 1
        if right >= len(html):
            raise UnclosedTagError('Reached end of file before tag was closed.')
    tag_name = html[left:right]
    if tag_name == '':
        # catches: </>
        raise InvalidTagNameError('Tag name cannot be the empty string')
    if html[right] != '>' and html[right] != ' ':
        raise PostconditionError('The postcondtion of get_closing_tag_name() is that right must be \
pointed at either a ">" or a " "')
    return tag_name, right
    
# an opening tag name is defined as a sequence of valid tag name characters
# preceded by a '<' and followed by a ' ' or a '>'
def get_opening_tag_name(html, i):
    if html[i] != '<':
        raise PreconditionError('The precondition of get_opening_tag_name() is that i must be \
pointed at a "<"')
    left, right = i+1, i+1
    # either reach the end of the tag or the beginning of the attributes
    while html[right] != '>' and html[right] != ' ':
        if html[right] not in VALID_TAG_CHARS:
            raise InvalidTagCharacterError(f'The character {html[right]} is not a valid tag character.')
        right += 1
        if right >= len(html):
            raise UnclosedTagError('Reached end of file before tag was closed.')
    tag_name = html[left:right]
    if tag_name == '':
        # catches: <> < > < class=someclass>
        raise InvalidTagNameError('Tag name cannot be the empty string')
    if html[right] != '>' and html[right] != ' ':
        raise PostconditionError('The postcondtion of get_opening_tag_name() is that right must be \
pointed at either a ">" or a " "')
    return tag_name, right

def consume_text(html, i, stack):
    if html[i] != '>':
        raise PreconditionError('The precondition of consume_text() is that i must be pointed \
at a "<"')
    text, i = get_text(html, i)
    if text != None:
        text_node = TextNode(text)
        stack[-1].addChild(text_node)
    if html[i] != '<':
        raise PostconditionError('The postcondition of consume_text() is that i must be pointed at a "<"')
    return i

def get_text(html, i):
    if html[i] != '>':
        raise PreconditionError('The precondition of get_text() is that i must be \
pointed at a "<"')
    left = i+1
    right = i+1 
    while html[right] != '<':
        if html[right] not in VALID_TEXT_CHARS:
            raise InvalidTextCharacterError(f'Character {html[right]} is not a valid text character.')
        right += 1
        if right >= len(html):
            raise MissingClosingTagError('Reached end of file without finding a closing tag.')
    text = html[left:right]
    text = text.strip()
    if text == '':
        return None, right
    if html[right] != '<':
        raise PostconditionError('The postcondition of get_text() is that right must be pointed at a "<"')
    return text, right

def get_attributes(html, i):
    if html[i] != ' ':
        raise PreconditionError('The precondition of get_attributes() is that i must be \
pointed at a " "')
    attrs = {}
    while html[i] != '>':
        key, value, i = get_attribute(html, i)
        attrs[key] = value
    if html[i] != '>':
        raise PostconditionError('The postcondition of get_attributes() is that i must be \
pointed at a ">"')
    return attrs, i

def get_attribute(html, i):
    if html[i] != ' ':
        raise PostconditionError('The precondition of get_attribute() is that i \
    must be be pointed at a " "')
    # catches: <div  class=value>, <div >, <div class=value  id=key>
    # (two spaces in the first and third cases above)
    if html[i+1].isspace() or html[i+1] == '>':
        raise WhitespaceError()
    left = i+1
    right = i+1
    # Get key
    while html[right] != '=':
        if html[right].isspace(): # catches: <div clas s=value>
            raise WhitespaceError('key name can\'t have a space in it')
        elif html[right] == '>': # catches: <div class></div>
            raise InvalidAttributeError("Expected a =")
        elif html[right] not in VALID_KEY_CHARS:
            raise InvalidKeyCharacterError(f'Character {html[right]} is not a valid key character.')
        right += 1
    key = html[left:right]
    right += 1
    left = right
    if html[right] == '"':
        value, right = get_quoted_value(html, left, right)
    else:
        value, right = get_unquoted_value(html, left, right)
    if html[right] != ' ' and html[right] != '>':
        raise PostconditionError('The postcondition of get_attribute() is that right \
must be pointed at either a " " or a ">"')
    return key, value, right

def get_unquoted_value(html, left, right):
    if html[right] not in VALID_VALUE_CHARS:
        raise PreconditionError('The precondition of get_unquote_value() is that right must be \
pointed at a valid value character.')
    while html[right] != ' ' and html[right] != '>':
        if html[right] not in VALID_VALUE_CHARS:
            raise InvalidValueCharacterError(f'Character {html[right]} is not a valid value character.')
        right += 1
    value = html[left:right]
    if value == '': # catches: <div class=></div>, <div class= ></div>, <title class= thetitle>Document</title>
        raise InvalidValueError('Attribute value cannot be the empty string')
    if html[right] != ' ' and html[right] != '>':
        raise PostconditionError('The postcondition of get_unquoted_value() is that right \
must be pointed at a " " or a ">"')
    return value, right

def get_quoted_value(html, left, right):
    if html[right] != '"':
        raise PreconditionError("The precondition of get_quoted_value() is that right must be \
pointed at a \"")
    left, right = left+1, right+1
    while html[right] != '"':
        if html[right].isspace():
            raise WhitespaceError()
        elif html[right] == '>':
            raise MissingClosingQuoteError("Expected a \"")
        elif html[right] not in VALID_VALUE_CHARS:
            raise InvalidValueCharacterError(f'Character {html[right]} is not a valid value character.')
        else:
            right += 1
    value = html[left:right]
    right += 1
    # catches: <div class="value"">, <div class="value"a>
    if html[right] != ' ' and html[right] != '>':
        raise InvalidAttributeFormatError('Expected a space " " or a ">"')
    if value == '': # catches <div class="">
        raise InvalidValueError('value can\'t be the empty string')
    if html[right] != ' ' and html[right] != '>':
        raise PostconditionError('The postcondition of get_unquoted_value() is that right \
must be pointed at a " " or a ">"')
    return value, right