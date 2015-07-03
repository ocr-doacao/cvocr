from subprocess import call
import os

def call_tesseract(filename, ext):
    call(["tesseract", "-l", "por", "-psm", "7", filename + ext, filename], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))