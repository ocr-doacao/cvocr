__author__ = 'andre'

from patterns import file_get_contents
from os import listdir
from os.path import isfile, join, splitext
import argparse
import re

def validator(validador, name, content):
    if validador:
        print content

def main():
    parser = argparse.ArgumentParser(description='Computer Visual module.')
    parser.add_argument('-p', '--path', metavar='image', type=str, required=True, help='Input file')
    args = parser.parse_args()
    path = args.path

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for fname in onlyfiles:
        (name, extension) = splitext(fname)
        if extension == ".txt":
            content = file_get_contents(join(path, name+extension))
            cnpj_re = re.compile('[0-9]][0-9]]/[0-9]][0-9]].[0-9]][0-9]][0-9]][0-9]]')
            validator(cnpj_re.match(content), join(path, name), content)

if __name__ == "__main__":
    main()