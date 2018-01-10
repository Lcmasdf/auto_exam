import lxml.html as h


def parse_form(html_str):
    tree = h.fromstring(html_str)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data