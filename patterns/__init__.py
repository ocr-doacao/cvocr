__author__ = 'andre'


def file_get_contents(fname):
    with open(fname, 'r') as content_file:
        return content_file.read()


class Validator:
    def __init__(self):
        self.patterns = []
        self.patterns.append((re.compile('CNPJ.*'), 'cnpj'))
        self.patterns.append((re.compile('.NPJ.*'), 'cnpj'))
        self.patterns.append((re.compile('C.PJ.*'), 'cnpj'))
        self.patterns.append((re.compile('CN.J.*'), 'cnpj'))
        self.patterns.append((re.compile('CNP.*') , 'cnpj'))
        self.patterns.append((re.compile('[0-9]*'), 'data'))

    def validate(self, content):
        for er, key in self.patterns:
            if re.match(content):
                print content
                yield key, content
