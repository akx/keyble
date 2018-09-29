# -- encoding: UTF-8 --
import argparse
import json
import pickle

from keyble.ocr_frontend import ocr_card_image_directory


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--cards-dir', required=True)
    ap.add_argument('-j', '--output-json')
    ap.add_argument('-p', '--output-pickle')
    args = ap.parse_args()

    if not (args.output_json or args.output_pickle):
        ap.error('some output is required (-j or -p)')

    results = ocr_card_image_directory(args.cards_dir)

    if args.output_json:
        with open(args.output_json, "w", encoding="UTF-8") as outf:
            json.dump(results, outf, indent=2, ensure_ascii=False)

    if args.output_pickle:
        with open(args.output_pickle, "wb") as outf:
            pickle.dump(results, outf, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
