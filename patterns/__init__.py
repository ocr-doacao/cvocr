__author__ = 'andre'

import re
import os

def file_get_contents(fname):
    with open(fname, 'r') as content_file:
        return content_file.read()

def clean_dir(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


class Validator:
    def __init__(self):
        self.patterns = []
        self.patterns.append((re.compile('CNPJ.*'), 'cnpj'))
        self.patterns.append((re.compile('.NPJ.*'), 'cnpj'))
        self.patterns.append((re.compile('C.PJ.*'), 'cnpj'))
        self.patterns.append((re.compile('CN.J.*'), 'cnpj'))
        self.patterns.append((re.compile('CNP.*'), 'cnpj'))
        # self.patterns.append((re.compile('[0-9]*'), 'data'))

    def validate(self, content):
        for er, key in self.patterns:
            if er.match(content):
                yield key, content
