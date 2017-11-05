import argparse
import os

import app


def main():
    parser = argparse.ArgumentParser(description='Compare pipeline inspection data given as csv files')
    parser.add_argument('--old', required=True, help='path to the csv file coming from the old inspection')
    parser.add_argument('--new', required=True, help='path to the csv file coming from the new inspection')
    parser.add_argument('--reverse', action='store_true',
                        help='print sections based on old boxes')
    args = parser.parse_args()

    if not os.path.isfile(args.old):
        print '--old arguments must be a valid file path'
        return
    if not os.path.isfile(args.new):
        print '--new arguments must be a valid file path'
        return

    app.ndtest(args.old, args.new, args.reverse)


if __name__ == "__main__":
    main()
