from html_parsing.html_parser import ElementNode, TextNode

# corresponds to test1.html
def dom1():
    root = ElementNode('html')
    head = ElementNode('head')
    body = ElementNode('body')
    root.children.append(head)
    root.children.append(body)
    title = ElementNode('title')
    title_attrs = {'class': 'thetitle'}
    title.attributes = title_attrs
    title_text = TextNode('Document')
    title.children.append(title_text)
    head.children.append(title)
    return root