__author__ = 'andre'

def file_get_contents(fname):
    with open(fname, 'r') as content_file:
        return content_file.read()