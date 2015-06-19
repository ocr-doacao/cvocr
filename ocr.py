__author__ = 'andre'

from ocr import call_tesseract
from os import listdir
from os.path import isfile, join, splitext
import argparse

def main():
    parser = argparse.ArgumentParser(description='Computer Visual module.')
    parser.add_argument('-p', '--path', metavar='image', type=str, required=True, help='Input file')
    args = parser.parse_args()
    path = args.path

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for fname in onlyfiles:
        (name, extension) = splitext(fname)
        if extension == ".png":
            call_tesseract(join(path, name), extension)

if __name__ == "__main__":
    main()