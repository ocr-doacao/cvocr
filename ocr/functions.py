from subprocess import call

def call_tesseract(filename, ext):
    call(["tesseract", "-l", "por", "-psm", "7", filename + ext, filename])