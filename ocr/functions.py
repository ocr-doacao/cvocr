from subprocess import call
from os import devnull


def call_tesseract(filename, ext):
    call(["tesseract", "-l", "ocr", "-psm", "8", filename + ext, filename], stdout=open(devnull, 'wb'),
         stderr=open(devnull, 'wb'))
