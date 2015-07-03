__author__ = 'andre'

from patterns import file_get_contents, Validator
from os import listdir
from os.path import isfile, join, splitext
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Computer Visual module.')
    parser.add_argument('-p', '--path', metavar='image', type=str, required=True, help='Input file')
    args = parser.parse_args()
    path = args.path

    only_files = [f for f in listdir(path) if isfile(join(path, f))]
    val = Validator()
    result = {}
    for fname in only_files:
        (name, extension) = splitext(fname)
        if extension == ".txt":
            content = file_get_contents(join(path, name+extension))
            for key, value in val.validate(content):
                result[key] = value
    print json.dumps(result)

if __name__ == "__main__":
    main()