# -- encoding: UTF-8 --
import argparse
import json
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=True)
    args = ap.parse_args()

    with open(args.file, 'r') as infp:
        data = json.load(infp)

    results_by_file = defaultdict(list)

    for result in data:
        for line in result['lines']:
            if line['confidence'] >= 50:
                results_by_file[result['filename']].append(line['text'])

    for filename, texts in sorted(results_by_file.items()):
        print(filename, texts)


if __name__ == '__main__':
    main()
