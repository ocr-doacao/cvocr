__author__ = 'andre'

from cv.cv import CVUtil
from ocr.functions import call_tesseract
from patterns import Validator, file_get_contents, clean_dir
from os import listdir
from os.path import isfile, join, splitext
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Computer Visual module.')
    parser.add_argument('-f', '--file', metavar='image', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--out', metavar='directory', type=str, required=True, help='Valid output directory')
    args = parser.parse_args()
    path = args.out

    clean_dir(path)

    cvu = CVUtil(args.file, path, False)
    cvu.optimized_close()
    cvu.cutter()

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    val = Validator()
    result = {'cnpj': None, 'data': None, 'coo': None, 'total': None}
    for fname in onlyfiles:
        (name, extension) = splitext(fname)
        if extension == ".png":
            call_tesseract(join(path, name), extension)
            content = file_get_contents(join(path, name+".txt"))
            for key, value in val.validate(content):
                result[key] = value
    print json.dumps(result)

if __name__ == "__main__":
    main()