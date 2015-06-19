__author__ = 'andre'

from cv.cv_util import CVUtil
import argparse

def main():
    parser = argparse.ArgumentParser(description='Computer Visual module.')
    parser.add_argument('-f', '--file', metavar='image', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--out', metavar='directory', type=str, required=True, help='Valid output directory')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        print "Verbosity turned on"

    cvu = CVUtil(args.file, args.out, args.verbose)
    cvu.optimized_close()
    cvu.cutter()

if __name__ == "__main__":
    main()